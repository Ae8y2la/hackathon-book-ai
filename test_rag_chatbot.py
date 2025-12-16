import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.config.settings import settings


def test_health_check():
    """Test the health check endpoint."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "services" in data


def test_root_endpoint():
    """Test the root endpoint."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert settings.app_version in data["version"]


def test_chat_endpoint_exists():
    """Test that chat endpoint is defined (even if it requires authentication/data)."""
    with TestClient(app) as client:
        # This should return 422 (validation error) or 405 (method not allowed) rather than 404
        response = client.post("/api/v1/chat")
        assert response.status_code in [405, 422]  # Method not allowed or validation error is expected


def test_ingestion_endpoint_exists():
    """Test that ingestion endpoint is defined (even if it requires authentication/data)."""
    with TestClient(app) as client:
        # This should return 422 (validation error) or 405 (method not allowed) rather than 404
        response = client.post("/api/v1/ingest")
        assert response.status_code in [405, 422]  # Method not allowed or validation error is expected


if __name__ == "__main__":
    pytest.main([__file__])