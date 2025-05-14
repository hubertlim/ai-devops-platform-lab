"""Custom middleware for correlation IDs and request logging."""

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger()

# Context variable for correlation ID
_correlation_id_ctx: dict[str, str] = {}


def get_correlation_id() -> str:
    """Get the current correlation ID."""
    return _correlation_id_ctx.get("correlation_id", "unknown")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Extracts or generates a correlation ID for each request."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        _correlation_id_ctx["correlation_id"] = correlation_id

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with structured fields."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        correlation_id = get_correlation_id()

        logger.info(
            "request_completed",
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            correlation_id=correlation_id,
            client_ip=request.client.host if request.client else "unknown",
        )

        return response
