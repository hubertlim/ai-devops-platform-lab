"""Metrics endpoint tests."""

import pytest


@pytest.mark.asyncio
async def test_metrics_endpoint_returns_prometheus_format(client):
    """Metrics endpoint should return Prometheus text format."""
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Should contain at least the default Python metrics
    assert "python_info" in response.text or "http_requests_total" in response.text


@pytest.mark.asyncio
async def test_metrics_contains_custom_metrics(client):
    """After making requests, custom metrics should appear."""
    # Make a request to generate metrics
    await client.post("/api/v1/completions", json={"prompt": "test"})

    response = await client.get("/metrics")
    body = response.text
    assert "ai_requests_total" in body
    assert "ai_request_duration_seconds" in body
