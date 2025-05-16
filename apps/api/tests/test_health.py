"""Health endpoint tests."""

import pytest


@pytest.mark.asyncio
async def test_health_returns_200(client):
    """Health check should return 200 with service info."""
    response = await client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "service" in data


@pytest.mark.asyncio
async def test_health_includes_environment(client):
    """Health check should include the current environment."""
    response = await client.get("/health")
    data = response.json()
    assert data["environment"] == "test"
