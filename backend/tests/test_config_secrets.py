"""Tests for configuration and secret handling.

Secrets (DATABASE_URL, ANTHROPIC_API_KEY) are stored as pydantic SecretStr so
they are masked in repr(), str(), logs and serialised settings, and never
appear in API responses. All secret values below are fake test strings.
"""

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.core.config import Settings, get_settings
from app.main import app

FAKE_API_KEY = "sk-ant-test-FAKE-key-1234567890"
FAKE_DB_URL = "postgresql://fake_user:fake-db-pass-987@localhost:5432/supplymind"
FAKE_SECRETS = (FAKE_API_KEY, FAKE_DB_URL, "fake-db-pass-987")


@pytest.fixture
def secret_env(monkeypatch):
    """Set fake secrets in the environment."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", FAKE_API_KEY)
    monkeypatch.setenv("DATABASE_URL", FAKE_DB_URL)


@pytest.fixture
def settings_with_secrets(secret_env):
    return Settings(_env_file=None)


@pytest.fixture
def app_with_secrets(secret_env):
    """Make get_settings() (used by the endpoints) return fake secrets."""
    get_settings.cache_clear()
    yield TestClient(app)
    get_settings.cache_clear()


# --- Non-secret settings are preserved -------------------------------------


def test_non_secret_defaults_preserved(monkeypatch):
    for name in ("APP_NAME", "APP_ENV", "APP_VERSION", "APP_DESCRIPTION", "DEBUG"):
        monkeypatch.delenv(name, raising=False)
    settings = Settings(_env_file=None)
    assert settings.app_name == "SupplyMind AI"
    assert settings.app_env == "development"
    assert settings.app_version == "0.1.0"
    assert "supply chain" in settings.app_description.lower()
    assert settings.debug is False


def test_non_secret_settings_are_plain_values(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Custom Name")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    settings = Settings(_env_file=None)
    assert settings.app_name == "Custom Name"
    assert settings.app_version == "9.9.9"
    assert isinstance(settings.app_name, str)


def test_get_settings_is_cached():
    get_settings.cache_clear()
    try:
        assert get_settings() is get_settings()
    finally:
        get_settings.cache_clear()


# --- Secrets are SecretStr and usable ---------------------------------------


def test_secrets_are_secretstr(settings_with_secrets):
    assert isinstance(settings_with_secrets.anthropic_api_key, SecretStr)
    assert isinstance(settings_with_secrets.database_url, SecretStr)


def test_secret_values_retrievable_explicitly(settings_with_secrets):
    assert settings_with_secrets.anthropic_api_key.get_secret_value() == FAKE_API_KEY
    assert settings_with_secrets.database_url.get_secret_value() == FAKE_DB_URL


# --- Secrets never appear in representations --------------------------------


def _assert_no_secrets(text: str) -> None:
    for secret in FAKE_SECRETS:
        assert secret not in text


def test_secrets_masked_in_repr_and_str(settings_with_secrets):
    _assert_no_secrets(repr(settings_with_secrets))
    _assert_no_secrets(str(settings_with_secrets))
    _assert_no_secrets(repr(settings_with_secrets.anthropic_api_key))
    _assert_no_secrets(str(settings_with_secrets.database_url))
    assert "**********" in str(settings_with_secrets.anthropic_api_key)


def test_secrets_masked_in_serialisation(settings_with_secrets):
    _assert_no_secrets(settings_with_secrets.model_dump_json())
    _assert_no_secrets(str(settings_with_secrets.model_dump()))
    _assert_no_secrets(f"{settings_with_secrets}")


# --- Secrets never appear in API responses ----------------------------------


@pytest.mark.parametrize("path", ["/", "/health", "/project-info", "/openapi.json"])
def test_endpoints_do_not_expose_secrets(app_with_secrets, path):
    # Sanity check: the endpoints really are using the fake secrets.
    assert get_settings().anthropic_api_key.get_secret_value() == FAKE_API_KEY

    response = app_with_secrets.get(path)
    assert response.status_code == 200
    _assert_no_secrets(response.text)
    lowered = response.text.lower()
    assert "anthropic_api_key" not in lowered
    assert "database_url" not in lowered
