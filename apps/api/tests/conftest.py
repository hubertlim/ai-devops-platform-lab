"""Test fixtures and configuration."""

import os

import pytest
from httpx import ASGITransport, AsyncClient

# Set test environment before importing app
os.environ["APP_ENV"] = "test"
os.environ["AI_PROVIDER"] = "mock"

from src.main import app  # noqa: E402


@pytest.fixture
async def client():
    """Async HTTP client for testing."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
