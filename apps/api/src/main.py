"""AI DevOps Platform Lab - FastAPI Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.middleware import CorrelationIdMiddleware, RequestLoggingMiddleware
from src.observability import setup_telemetry
from src.routes import ai, health, metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: setup and teardown."""
    setup_telemetry()
    yield


app = FastAPI(
    title="AI DevOps Platform Lab",
    version=settings.app_version,
    docs_url="/docs",
    lifespan=lifespan,
)

# Middleware (order matters: outermost first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

# Routes
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(ai.router, prefix="/api/v1")
