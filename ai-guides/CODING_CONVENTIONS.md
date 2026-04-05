# Coding Conventions

_Changelog: 2026-04-05 - Initial version._

## Python

- **Naming**: `snake_case` for variables and functions. `PascalCase` for classes.
- **Type Hints**: Mandatory for all function signatures and variable declarations.
- **Models**: Use Pydantic for data validation and settings management. FastAPI request/response models should be Pydantic models.
- **Async**: Use `async/await` for all I/O-bound operations, especially database access and external API calls.
- **Dependency Injection**: Use FastAPI's dependency injection system (`Depends`) for database sessions, configuration, and other shared resources like `get_current_user`.

## SQLModel

- **Table Naming**: Tables should be plural and in `snake_case` (e.g., `log_records`).
- **Model Naming**: SQLModel classes should be singular and in `PascalCase` (e.g., `LogRecord`).
- **Relationships**: Clearly define relationships using `Relationship` and `Field(foreign_key=...)`.
- **Indexes**: Add indexes (`index=True`) to foreign keys and columns frequently used in `WHERE` clauses (e.g., `email`, `phone`).

## Testing (Pytest)

- **Structure**: Tests should mirror the application structure (e.g., `tests/test_auth.py` and future route-specific modules).
- **Fixtures**: Use fixtures for setting up test data, database sessions, and API clients.
- **Mocking**: Use `unittest.mock` or `pytest-mock` for external services. Avoid mocking internal business logic where possible.
- **Coverage**: Aim for >80% test coverage. Critical business logic should be 100% covered.
- **Database**: Use a separate SQLite database for tests to ensure isolation.

## Error Handling

- **Custom Exceptions**: Define custom exception classes for specific business logic errors.
- **HTTP Exceptions**: Use FastAPI's `HTTPException` for standard HTTP errors.
- **Logging**:
  - `INFO`: General application flow.
  - `WARNING`: Recoverable errors or potential issues.
  - `ERROR`: Unrecoverable errors that require intervention. Log the full traceback.
  - `CRITICAL`: System-level failures.
- **Sensitive Data**: Never log raw secrets, passwords, or PII. Use anonymization helpers.
- **Middleware Order**: Be mindful of middleware execution order. Auth middleware runs first to populate `request.state.user`, which is then used by verification and admin middlewares.
