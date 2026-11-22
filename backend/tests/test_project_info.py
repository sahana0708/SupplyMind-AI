"""Tests for GET /project-info."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_project_info_returns_basic_details():
    response = client.get("/project-info")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "SupplyMind AI"
    assert body["version"]
    assert "supply chain" in body["description"].lower()
    assert body["stage"] == "Day 1 - Project foundation"


def test_project_info_lists_all_planned_modules():
    modules = client.get("/project-info").json()["planned_modules"]
    assert len(modules) == 9
    assert "Watcher Agent" in modules
    assert "Human Approval System" in modules


def test_project_info_does_not_expose_secrets():
    text = client.get("/project-info").text.lower()
    assert "api_key" not in text
    assert "database_url" not in text
    assert "password" not in text
