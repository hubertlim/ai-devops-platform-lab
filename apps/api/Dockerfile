# =============================================================================
# Backend API - Multi-stage Dockerfile
# =============================================================================

# ---------------------------------------------------------------------------
# Base stage: shared dependencies
# ---------------------------------------------------------------------------
FROM python:3.12-slim@sha256:090ba77e2958f6af52a5341f788b50b032dd4ca28377d2893dcf1ecbdfdfe203 AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.lock .
RUN pip install --no-cache-dir --require-hashes -r requirements.lock

# ---------------------------------------------------------------------------
# Development stage: hot-reload with source mounted
# ---------------------------------------------------------------------------
FROM base AS development

COPY requirements-dev.lock .
RUN pip install --no-cache-dir --require-hashes --no-deps -r requirements-dev.lock

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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail --silent http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
