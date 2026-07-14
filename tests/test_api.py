"""
Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()


def test_metrics_endpoint():
    """Test metrics endpoint."""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert "evaluator_statistics" in response.json()


def test_history_endpoint():
    """Test history endpoint."""
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    assert "history" in response.json()


def test_traces_endpoint():
    """Test traces endpoint."""
    response = client.get("/api/v1/traces")
    assert response.status_code == 200
    assert "format" in response.json()
