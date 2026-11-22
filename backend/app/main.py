"""SupplyMind AI - FastAPI application entry point.

Creates the FastAPI app and registers route modules. Feature modules
(agents, risk engine, MCP server, etc.) will be attached here as they are built.
"""

from fastapi import FastAPI

from app.api.routes import system
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

app.include_router(system.router)
