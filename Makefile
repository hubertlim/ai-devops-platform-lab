.PHONY: help build up down test lint scan clean logs

COMPOSE := docker compose
REGISTRY ?= ghcr.io
IMAGE_PREFIX ?= hubertlim/ai-devops-platform-lab
VERSION ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "dev")

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Development
# ---------------------------------------------------------------------------

build: ## Build all Docker images
	$(COMPOSE) build

up: ## Start all services in background
	$(COMPOSE) up -d

down: ## Stop all services
	$(COMPOSE) down

restart: ## Restart all services
	$(COMPOSE) restart

logs: ## Tail logs from all services
	$(COMPOSE) logs -f

clean: ## Remove containers, volumes, and images
	$(COMPOSE) down -v --rmi local

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------

test: test-api test-web ## Run all tests

test-api: ## Run backend tests
	$(COMPOSE) run --rm api pytest tests/ -v

test-web: ## Run frontend tests
	$(COMPOSE) run --rm web npm run test -- --run

# ---------------------------------------------------------------------------
# Linting
# ---------------------------------------------------------------------------

lint: lint-api lint-web ## Run all linters

lint-api: ## Lint backend with Ruff
	$(COMPOSE) run --rm api ruff check src/ tests/

lint-web: ## Lint frontend with ESLint
	$(COMPOSE) run --rm web npm run lint

# ---------------------------------------------------------------------------
# Security Scanning
# ---------------------------------------------------------------------------

scan: scan-api scan-web ## Run all security scans

scan-api: build ## Scan backend container with Trivy
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy:latest image $(IMAGE_PREFIX)/api:$(VERSION)

scan-web: build ## Scan frontend container with Trivy
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy:latest image $(IMAGE_PREFIX)/web:$(VERSION)

scan-deps: ## Scan dependencies for vulnerabilities
	$(COMPOSE) run --rm api pip-audit
	$(COMPOSE) run --rm web npm audit --audit-level=moderate

# ---------------------------------------------------------------------------
# Infrastructure
# ---------------------------------------------------------------------------

tf-init: ## Initialize Terraform
	cd infra/terraform && terraform init

tf-plan: ## Plan Terraform changes
	cd infra/terraform && terraform plan -out=tfplan

tf-apply: ## Apply Terraform changes
	cd infra/terraform && terraform apply tfplan
