# Tech-Specific Notes

_Changelog: 2026-04-05 - Initial version._

## FastAPI & Pydantic

- **Validators**: Use Pydantic validators for complex field validation within models.
- **`model_dump()`**: Use `model_dump(by_alias=True, exclude_unset=True)` when returning data to respect model aliases and avoid sending `null` for optional fields that were not provided.
- **Background Tasks**: For fire-and-forget tasks that should not block the response, use `BackgroundTasks`.
- **Dependency Injection for Auth**: The `get_current_user` dependency in `app/utils/deps.py` uses `OAuth2PasswordBearer` to extract the token from the request and retrieve the user, making it available to all protected endpoints.

## Poetry

- **Dependency Groups**: Use dependency groups for managing development vs. production packages.
  - `poetry add <package>` for main dependencies.
  - `poetry add <package> --group dev` for development dependencies (e.g., `pytest`, `ruff`).
- **Scripts**: Define common commands in `pyproject.toml` under `[tool.poetry.scripts]`.
  - Example: `start = "uvicorn app.main:app --host 0.0.0.0 --port 8000"`
- **Running Commands**: Always run commands within the poetry environment using `poetry run <command>`.

## Redis

- **Rate Limiting**: Implement rate limiting middleware using a Redis-backed token bucket or fixed window algorithm.
- **Job Queues**: For long-running tasks, consider using a library like `arq` or `Celery` with a Redis broker.
- **Caching**: Use a simple `get/set` pattern with a TTL for caching database query results.
- **Session & OTP Store**: Redis is used to store session tokens with a TTL, allowing for easy revocation. It is also used to cache OTPs for email and phone verification with a short TTL (e.g., 10 minutes).

## Kubernetes

- **ConfigMaps & Secrets**: Mount configuration and secrets into pods as environment variables or files.
- **Probes**:
  - **Liveness Probe**: Points to `/health` to restart unhealthy pods.
  - **Readiness Probe**: Points to `/health` to ensure a pod is ready to receive traffic.
- **Deployments**: Use `Deployment` resources for stateless services and `StatefulSet` for services requiring stable network identifiers or persistent storage.

## CI/CD Pipeline

A typical pipeline sequence in `.github/workflows/ci.yml`:

1.  **Lint**: `poetry run ruff check .`
2.  **Test**: `poetry run pytest`
3.  **Build**: `docker build -t <image_name>:<tag> .`
4.  **Push**: `docker push <image_name>:<tag>`
5.  **Deploy**: `helm upgrade --install <release_name> ./helm -f ./helm/values.yaml`

## OAuth Implementation

- The OAuth flow is initiated by redirecting the user to the provider.
- The provider calls back to a dedicated endpoint (`/auth/oauth/{provider}/callback`).
- The callback handler verifies the user, creates or links the `Account` and `User` models, and establishes a session.
- Libraries like `httpx-oauth` are recommended for handling the complexities of different providers.
