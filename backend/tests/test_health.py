"""Tests for the Day 1 foundation: health endpoint and settings."""

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == "SupplyMind AI"
    assert "version" in body


def test_settings_read_from_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DEBUG", "true")
    settings = Settings(_env_file=None)
    assert settings.app_env == "testing"
    assert settings.debug is True


def test_env_file_points_to_project_root():
    from app.core.config import ENV_FILE, PROJECT_ROOT

    assert (PROJECT_ROOT / "CLAUDE.md").is_file()
    assert ENV_FILE == PROJECT_ROOT / ".env"


def test_secrets_have_no_hardcoded_defaults(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    settings = Settings(_env_file=None)
    assert settings.anthropic_api_key is None
    assert settings.database_url is None
