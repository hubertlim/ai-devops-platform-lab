"""Security validation tests."""

import pytest


@pytest.mark.asyncio
async def test_no_server_header_leak(client):
    """Server should not expose implementation details in headers."""
    response = await client.get("/health")
    # FastAPI/Uvicorn should not leak server version
    server_header = response.headers.get("server", "")
    assert "uvicorn" not in server_header.lower() or server_header == ""


@pytest.mark.asyncio
async def test_cors_preflight(client):
    """CORS preflight should respond correctly for allowed origins."""
    response = await client.options(
        "/api/v1/completions",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
async def test_invalid_json_returns_422(client):
    """Malformed JSON should return 422, not 500."""
    response = await client.post(
        "/api/v1/completions",
        content="not valid json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_sql_injection_in_prompt_handled(client):
    """SQL injection attempts in prompt should not cause errors."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "'; DROP TABLE users; --"},
    )
    # Should succeed (mock provider) without any server error
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_xss_in_prompt_handled(client):
    """XSS attempts in prompt should be handled safely."""
    response = await client.post(
        "/api/v1/completions",
        json={"prompt": "<script>alert('xss')</script>"},
    )
    assert response.status_code == 200
    # Response should not execute scripts (it's JSON)
    data = response.json()
    assert isinstance(data["text"], str)
