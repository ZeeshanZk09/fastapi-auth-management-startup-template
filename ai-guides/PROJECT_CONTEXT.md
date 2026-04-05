# Project Context

_Changelog: 2026-04-05 - Initial version._

## High-Level Architecture

- **Core Services**: Monolithic Python backend built with FastAPI.
- **Database**: PostgreSQL for persistent storage, accessed via SQLModel.
- **Cache**: Redis for caching, rate limiting, and potentially job queues.
- **Containerization**: Services are containerized using Docker and deployed to Kubernetes.
- **Communication**: RESTful APIs via FastAPI. Synchronous request/response model.
- **Authentication**: A complete auth-management system with registration, login, password reset, OAuth, and session management.

## Tech Stack Versions

- **Python**: `~3.11`
- **FastAPI**: `~0.135.3`
- **SQLModel**: `~0.0.38`
- **PostgreSQL**: `15+`
- **Poetry**: `1.x`
- **Uvicorn**: `~0.43.0`
- **Pandas**: `~3.0.2`
- **Pytest**: `~9.0.2`

## Environment Variables

- Handled via `app/config.py` (`pydantic-settings`) and loaded from `.env` and process environment variables.
- Secrets should be loaded from environment variables or a secrets management system (e.g., Kubernetes Secrets) and not be hardcoded.
- **`DATABASE_URL`**: Primary connection string for PostgreSQL. Example: `postgresql://user:password@host:port/dbname`
- **`REDIS_URL`**: Connection string for Redis. Example: `redis://localhost:6379`
- **`SECRET_KEY`**: A secret key for signing JWTs.
- **`GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`**: OAuth credentials for Google.
- **`GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`**: OAuth credentials for GitHub.
- **`EMAIL_DELIVERY_ENABLED`, `SMTP_*`**: Email sending controls and SMTP configuration.
- **`SMS_DELIVERY_ENABLED`, `TWILIO_*`**: SMS sending controls and Twilio configuration.

## Folder Structure

- **`/app`**: Main application source code.
  - **`/app/routes`**: FastAPI routers for different API endpoints (auth, users, admin, oauth).
  - **`/app/models`**: SQLModel table definitions (User, Session, Account) and enums.
  - **`/app/controllers`**: Business logic for handling requests.
  - **`/app/middlewares`**: Request middleware for authentication and authorization.
  - **`/app/utils`**: Utility modules (email, sms, jwt, redis, password hashing, dependencies).
  - **`/app/schemas`**: Pydantic schemas for request/response validation.
  - **`/app/config.py`**: Environment settings model.
  - **`/app/database.py`**: SQLModel engine/session and metadata bootstrap.
  - **`/app/gunicorn_conf.py`**: Gunicorn runtime settings.
- **`/tests`**: Pytest tests.
- **`/helm`**: Kubernetes Helm charts for deployment.
- **`/ai-guides`**: Living documentation for AI assistant collaboration.
- **`docker-compose.yml`**: Local development environment setup.
