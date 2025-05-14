"""Prometheus metrics endpoint."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
)

router = APIRouter(tags=["metrics"])

# Metrics definitions
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

AI_REQUESTS = Counter(
    "ai_requests_total",
    "Total AI completion requests",
    ["provider", "status"],
)

AI_LATENCY = Histogram(
    "ai_request_duration_seconds",
    "AI request latency in seconds",
    ["provider"],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)


@router.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics() -> str:
    """Expose Prometheus-compatible metrics."""
    return generate_latest().decode("utf-8")
