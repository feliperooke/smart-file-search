import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():

    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_check_wrong_method():
    response = client.post("/api/health/")
    assert response.status_code == 405