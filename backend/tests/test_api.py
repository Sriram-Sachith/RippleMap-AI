"""
Integration tests for API endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["service"] == "RippleMap AI"
    assert "documentation" in data


@pytest.mark.asyncio
async def test_status_endpoint(client):
    """Test status endpoint."""
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "active"
    assert "environment" in data


@pytest.mark.asyncio
async def test_api_documentation(client):
    """Test API documentation endpoint."""
    response = await client.get("/api/docs")
    assert response.status_code == 200
