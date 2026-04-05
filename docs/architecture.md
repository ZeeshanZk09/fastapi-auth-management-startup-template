# Architecture Overview

## Runtime Topology

- FastAPI application starts in `app/main.py`.
- Route modules are loaded from `app/routes/`.
- Global settings are loaded from environment variables by `app/config.py`.

## Configuration Flow

1. `Settings` in `app/config.py` loads values from `.env` (if present) and environment variables.
2. `DATABASE_URL` and `REDIS_URL` configure persistence and Redis access.
3. `IS_LOCAL` controls local-friendly behavior such as SQL query echo in `app/database.py`.

## Data Layer

- SQLModel engine/session helpers are in `app/database.py`.
- SQLModel models are in `app/models/`.
- Default DB URL is `sqlite:///./app.db`, override with `DATABASE_URL`.

## Authentication

- JWT creation/validation is in `app/utils/jwt.py`.
- OAuth controllers are in `app/controllers/oauth_controller.py`.
- Dependency providers (`get_session`, `get_current_user`, `get_redis`) are in `app/utils/deps.py`.

## Testing

- Test framework: pytest
- Main tests: `tests/test_auth.py`
- Test env bootstrap: `tests/conftest.py`

## CI/CD

- GitHub Actions workflow: `.github/workflows/ci.yml`
- CI installs the package and runs pytest on push/pull request.
