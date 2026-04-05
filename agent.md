# Agent Quickstart

## Environment

Use the existing virtual environment for all commands.

Windows PowerShell:

```powershell
.venv\Scripts\python -m pytest -q
```

Git Bash:

```bash
.venv/Scripts/python -m pytest -q
```

## High-level Architecture

- `app/main.py`: FastAPI app creation and router registration
- `app/routes/`: HTTP endpoints (`auth`, `users`, `admin`, `oauth`)
- `app/config.py`: central environment-driven settings
- `app/database.py`: SQLModel engine/session and DB bootstrap
- `app/models/`: SQLModel ORM tables
- `tests/`: pytest suite for authentication flows

## Data Layer

- Engine/session helpers: `app/database.py`
- SQLModel tables: `app/models/user.py`, `app/models/session.py`, `app/models/account.py`
- Default DB URL: `sqlite:///./app.db`
- Override via env var: `DATABASE_URL`
- SQL echo is controlled by env var `IS_LOCAL`

## Typical Developer Workflow

1. Install/refresh deps in `.venv`.
2. Run tests: `python -m pytest -q`.
3. Make changes.
4. Re-run tests.

## CI

- GitHub Actions workflow: `.github/workflows/ci.yml`
- Runs tests on push/pull request.

## Guardrails

- Keep imports lightweight at module import time.
- Avoid hard runtime dependency on optional backends.
- Prefer SQLModel for persistence in this project.
- Keep tests warning-free.
