# SupplyMind AI

AI-powered enterprise operations and supply chain recovery platform.
It detects supply chain disruptions, investigates business impact and
recommends recovery actions.

## Current stage

Day 1 - project foundation: FastAPI backend skeleton, configuration and tests.
No database, agents, MCP, Temporal or frontend yet.

## Project layout

| Path | Purpose |
|---|---|
| `backend/app/main.py` | FastAPI application entry point; registers routes |
| `backend/app/core/config.py` | Settings loaded from environment variables / `.env` |
| `backend/app/api/routes/system.py` | `GET /`, `GET /health`, `GET /project-info` |
| `backend/app/{agents,database,mcp_server,models,schemas,services}` | Placeholders for upcoming modules |
| `backend/tests/` | Pytest test suite |
| `backend/pytest.ini` | Pytest configuration |
| `database/` | SQL schema and seed data (later stage) |
| `frontend/` | React + TypeScript dashboard (later stage) |
| `analytics/`, `docs/`, `scripts/` | Analytics, documentation, helper scripts |

## Prerequisites

- Windows with PowerShell
- Python 3.12 (check with `py -3.12 --version`)

## Setup (Windows, PowerShell)

Run these from the project root `C:\Users\sahan\SupplyMind-AI`.

1. Create the virtual environment (Python 3.12):

   ```powershell
   py -3.12 -m venv .venv
   ```

2. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Your prompt should now start with `(.venv)`.
   If PowerShell blocks the script, run this once and then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

3. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Create your local environment file in the project root (optional for Day 1):

   ```powershell
   Copy-Item .env.example .env
   ```

   Edit `.env` with your own values. Never commit `.env`.
   The app always reads `.env` from the project root, even when started
   from `backend`.

## Run the API

Open a PowerShell window, then:

```powershell
cd C:\Users\sahan\SupplyMind-AI
.\.venv\Scripts\Activate.ps1
cd backend
uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000/ - welcome message
- http://127.0.0.1:8000/health - health check
- http://127.0.0.1:8000/project-info - project information
- http://127.0.0.1:8000/docs - interactive API docs

Stop the server with `Ctrl+C`.

## Run tests

In a PowerShell window (a second one if the API is still running):

```powershell
cd C:\Users\sahan\SupplyMind-AI
.\.venv\Scripts\Activate.ps1
cd backend
pytest -v
```

## Deactivate the virtual environment

```powershell
deactivate
```

## Security

Never commit `.env` or hardcode passwords or API keys. All secrets are read
from environment variables. `.env.example` contains placeholders only.
