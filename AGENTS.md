# AGENTS

## Purpose

This repository is a FastAPI template with a lightweight SQLModel data layer and pytest-based tests.

## Directory Map

- `app/main.py`: app bootstrap
- `app/routes/`: API routes
- `app/config.py`: environment-driven settings
- `app/database.py`: SQLModel engine/session and table bootstrap
- `app/models/`: SQLModel tables
- `app/utils/`: utility helpers (deps, jwt, email, sms, redis)
- `tests/test_auth.py`: automated auth tests

## Non-negotiables

- Use SQLModel for persistence changes.
- Do not use PyMongo in this codebase.
- Run tests in `.venv` before finishing.
- Keep CI in GitHub Actions.

## Quick Commands

PowerShell:

```powershell
.venv\Scripts\python -m pytest -q
```

Git Bash:

```bash
.venv/Scripts/python -m pytest -q
```

## CI

- Workflow file: `.github/workflows/ci.yml`
- Triggered on push and pull request.
