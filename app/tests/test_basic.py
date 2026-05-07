"""Basic Tests"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """Tets simple health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Robot Payment Testing Platform" in response.json()["message"]


def test_api_health():
    """Test API health endpoint"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_mcdonalds():
    """Test McDonald's endpoint"""
    response = client.get("/api/v1/terminals/mcdonalds")
    assert response.status_code == 200
    assert response.json()["merchant"] == "McDonald's"


def test_grocery_regression():
    """Test grocery regression endpoint"""
    response = client.get("/api/v1/terminals/grocery/regression")
    assert response.status_code == 200
    assert response.json()["merchant"] == "Migros"
