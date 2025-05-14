"""AI completion endpoint with pluggable providers."""

import time

import structlog
from fastapi import APIRouter, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from src.config import settings
from src.middleware import get_correlation_id
from src.providers import get_provider
from src.routes.metrics import AI_LATENCY, AI_REQUESTS

router = APIRouter(tags=["ai"])
logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)


class CompletionRequest(BaseModel):
    """Request body for AI completion."""

    prompt: str = Field(..., min_length=1, max_length=4096, description="The input prompt")
    max_tokens: int = Field(default=256, ge=1, le=4096, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")


class CompletionResponse(BaseModel):
    """Response body for AI completion."""

    text: str
    provider: str
    model: str
    usage: dict
    correlation_id: str


@router.post("/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest) -> CompletionResponse:
    """Generate an AI completion from the configured provider."""
    with tracer.start_as_current_span("ai_completion") as span:
        correlation_id = get_correlation_id()
        span.set_attribute("ai.provider", settings.ai_provider)
        span.set_attribute("ai.max_tokens", request.max_tokens)
        span.set_attribute("correlation_id", correlation_id)

        provider = get_provider(settings.ai_provider)
        start_time = time.perf_counter()

        try:
            result = await provider.complete(
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )

            duration = time.perf_counter() - start_time
            AI_REQUESTS.labels(provider=settings.ai_provider, status="success").inc()
            AI_LATENCY.labels(provider=settings.ai_provider).observe(duration)

            logger.info(
                "ai_completion_success",
                provider=settings.ai_provider,
                duration_ms=round(duration * 1000, 2),
                correlation_id=correlation_id,
            )

            return CompletionResponse(
                text=result["text"],
                provider=settings.ai_provider,
                model=result["model"],
                usage=result["usage"],
                correlation_id=correlation_id,
            )

        except Exception as e:
            AI_REQUESTS.labels(provider=settings.ai_provider, status="error").inc()
            logger.error(
                "ai_completion_error",
                provider=settings.ai_provider,
                error=str(e),
                correlation_id=correlation_id,
            )
            raise HTTPException(status_code=502, detail="AI provider error") from e
