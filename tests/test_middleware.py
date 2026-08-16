"""Tests for LoggingMiddleware."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_response_has_request_id_header():
    """Middleware adds a unique X-Request-ID header."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0


def test_response_has_process_time_header():
    """Middleware adds X-Process-Time header with a numeric value."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) >= 0


def test_request_ids_are_unique_per_request():
    """Each request gets a distinct request id."""
    r1 = client.get("/health")
    r2 = client.get("/health")
    assert r1.headers["X-Request-ID"] != r2.headers["X-Request-ID"]
