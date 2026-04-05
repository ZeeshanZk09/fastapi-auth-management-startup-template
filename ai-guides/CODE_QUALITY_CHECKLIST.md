# Code Quality Checklist

_Changelog: 2026-04-05 - Initial version._

## Security

- [ ] **SQL Injection**: All database queries are executed via the SQLModel ORM, with no raw SQL concatenation.
- [ ] **Cross-Site Scripting (XSS)**: FastAPI's automatic JSON encoding and templating engine (if used) properly escape outputs.
- [ ] **Secrets Management**: No secrets, API keys, or passwords are present in source code or logs. They are loaded from environment variables or a vault.
- [ ] **Input Validation**: All incoming data is validated using Pydantic models.

## Performance

- [ ] **Database Indexes**: All foreign keys and frequently queried columns have database indexes.
- [ ] **Caching**: Expensive or frequently accessed data is cached in Redis.
- [ ] **Asynchronous Operations**: All I/O-bound calls (DB, network) are `async` and non-blocking.
- [ ] **Query Optimization**: Avoid N+1 query problems. Use `selectinload` for relationships where appropriate.

## Maintainability

- [ ] **Docstrings**: All public modules, classes, and functions have clear docstrings.
- [ ] **Separation of Concerns**: Business logic is separate from routing and data access.
- [ ] **Configuration**: Configuration is externalized and not hardcoded.
- [ ] **Dependency Injection**: Code relies on abstractions and injected dependencies, not concrete implementations.

## Docker & Kubernetes Readiness

- [ ] **Health Checks**: A `/health` or similar endpoint is implemented for liveness and readiness probes.
- [ ] **Resource Limits**: The application is mindful of memory and CPU usage.
- [ ] **Graceful Shutdown**: The application handles `SIGTERM` to shut down gracefully.
- [ ] **Statelessness**: The application is stateless where possible. State is managed in the database or Redis.
