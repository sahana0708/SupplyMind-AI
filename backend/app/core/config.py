"""Application settings.

All configuration is read from environment variables (or a local .env file).
Secrets such as passwords and API keys are never hardcoded here.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root = SupplyMind-AI/ (this file is backend/app/core/config.py).
# Using an absolute path means .env is found no matter which directory
# uvicorn or pytest is started from.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SupplyMind AI"
    app_env: str = "development"
    app_version: str = "0.1.0"
    app_description: str = (
        "AI-powered enterprise operations and supply chain recovery platform"
    )
    debug: bool = False

    # Secrets: optional until the database / Claude features are built.
    # SecretStr masks the value in repr(), str(), logs and model_dump_json();
    # call .get_secret_value() only at the point of use (e.g. creating the
    # database engine or the Anthropic client).
    database_url: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
