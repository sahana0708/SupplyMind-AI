"""Tests for GET / (welcome endpoint)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_welcome_message():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Welcome to SupplyMind AI API"


def test_root_lists_other_endpoints():
    body = client.get("/").json()
    assert body["docs"] == "/docs"
    assert body["health"] == "/health"
    assert body["project_info"] == "/project-info"
