# Claude Notes For This Repository

## Mission

Maintain and extend a FastAPI template with SQLModel persistence, clean tests, and GitHub Actions CI.

## Fast Facts

- Entry point: `app/main.py`
- Config settings: `app/config.py`
- Routers: `app/routes/auth.py`, `app/routes/users.py`, `app/routes/admin.py`, `app/routes/oauth.py`
- SQLModel engine/session: `app/database.py`
- SQLModel tables: `app/models/user.py`, `app/models/session.py`, `app/models/account.py`
- Tests: `tests/test_auth.py`

## Required Runtime Context

- Use existing `.venv` for all Python operations.
- Expected quick check command:
  - `.venv\Scripts\python -m pytest -q`

## Persistence Rules

- Do not reintroduce `pymongo`.
- Use SQLModel models for new persisted structures.
- Keep DB URL configurable with `DATABASE_URL`.

## CI Rules

- Use GitHub Actions (`.github/workflows/ci.yml`).
- Do not add GitLab CI files unless explicitly requested.

## Quality Rules

- Tests must pass before finishing.
- Keep pytest output warning-free when possible.
- Prefer small, isolated changes with clear file ownership.
