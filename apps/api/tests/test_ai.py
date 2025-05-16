"""AI completion endpoint tests."""

import pytest


@pytest.mark.asyncio
async def test_completion_success(client):
    """Valid prompt should return a completion."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "hello", "max_tokens": 100, "temperature": 0.5},
    )
    assert response.status_code == 200

    data = response.json()
    assert "text" in data
    assert data["provider"] == "mock"
    assert data["model"] == "mock-v1"
    assert "usage" in data
    assert data["usage"]["total_tokens"] > 0
    assert "correlation_id" in data


@pytest.mark.asyncio
async def test_completion_empty_prompt_rejected(client):
    """Empty prompt should be rejected with 422."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "", "max_tokens": 100},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_completion_prompt_too_long(client):
    """Prompt exceeding max length should be rejected."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "x" * 5000, "max_tokens": 100},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_completion_invalid_temperature(client):
    """Temperature outside valid range should be rejected."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "test", "temperature": 5.0},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_completion_correlation_id_propagated(client):
    """Correlation ID from request header should appear in response."""
    correlation_id = "test-correlation-123"
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "hello"},
        headers={"X-Correlation-ID": correlation_id},
    )
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") == correlation_id
    assert response.json()["correlation_id"] == correlation_id
