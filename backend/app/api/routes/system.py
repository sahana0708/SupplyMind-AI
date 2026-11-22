"""System endpoints: welcome message, health check and project information.

These endpoints do not touch the database or any external service.
They never return secrets (API keys, database URLs).
"""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["system"])

# Planned platform modules (from CLAUDE.md). Status is "planned" until built.
PLANNED_MODULES = [
    "Watcher Agent",
    "Commander Agent",
    "Financial Risk Engine",
    "Supplier Recommendation Engine",
    "MCP Server",
    "Workflow Orchestration",
    "Human Approval System",
    "Analytics Dashboard",
    "Audit Logging",
]


@router.get("/")
def root() -> dict:
    """Welcome message with pointers to the other endpoints."""
    settings = get_settings()
    return {
        "message": f"Welcome to {settings.app_name} API",
        "docs": "/docs",
        "health": "/health",
        "project_info": "/project-info",
    }


@router.get("/health")
def health() -> dict:
    """Liveness check: confirms the API process is running."""
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get("/project-info")
def project_info() -> dict:
    """Basic, non-sensitive information about the project."""
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "environment": settings.app_env,
        "stage": "Day 1 - Project foundation",
        "planned_modules": PLANNED_MODULES,
    }
