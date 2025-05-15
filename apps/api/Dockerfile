# =============================================================================
# Backend API - Multi-stage Dockerfile
# =============================================================================

# ---------------------------------------------------------------------------
# Base stage: shared dependencies
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Development stage: hot-reload with source mounted
# ---------------------------------------------------------------------------
FROM base AS development

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------------------------------------------------------------------------
# Production stage: minimal image
# ---------------------------------------------------------------------------
FROM base AS production

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
