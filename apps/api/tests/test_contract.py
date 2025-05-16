"""API contract tests.

These tests verify the API response schema matches the documented contract.
They serve as a lightweight alternative to full OpenAPI schema validation.
"""

import pytest


@pytest.mark.asyncio
async def test_completion_response_contract(client):
    """Completion response must match the documented schema."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "test contract"},
    )
    assert response.status_code == 200

    data = response.json()

    # Required fields
    assert "text" in data
    assert "provider" in data
    assert "model" in data
    assert "usage" in data
    assert "correlation_id" in data

    # Type checks
    assert isinstance(data["text"], str)
    assert isinstance(data["provider"], str)
    assert isinstance(data["model"], str)
    assert isinstance(data["correlation_id"], str)

    # Usage sub-schema
    usage = data["usage"]
    assert "prompt_tokens" in usage
    assert "completion_tokens" in usage
    assert "total_tokens" in usage
    assert isinstance(usage["prompt_tokens"], int)
    assert isinstance(usage["completion_tokens"], int)
    assert isinstance(usage["total_tokens"], int)
    assert usage["total_tokens"] == usage["prompt_tokens"] + usage["completion_tokens"]


@pytest.mark.asyncio
async def test_health_response_contract(client):
    """Health response must match the documented schema."""
    response = await client.get("/health")
    assert response.status_code == 200

    data = response.json()

    # Required fields
    required_fields = ["status", "service", "version", "environment"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
        assert isinstance(data[field], str), f"Field {field} must be a string"

    # Status must be a known value
    assert data["status"] in ["healthy", "degraded", "unhealthy"]


@pytest.mark.asyncio
async def test_error_response_contract(client):
    """Error responses must follow a consistent format."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": ""},  # Invalid: empty prompt
    )
    assert response.status_code == 422

    data = response.json()
    # FastAPI validation errors follow this structure
    assert "detail" in data
