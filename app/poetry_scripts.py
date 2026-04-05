import os
import subprocess
from typing import Sequence


LOCAL_DEV_DATABASE_URL = "sqlite:///./app.db"


def _run(command: Sequence[str]) -> int:
    try:
        result = subprocess.run(command, check=False)
        return int(result.returncode)
    except KeyboardInterrupt:
        return 130


def _is_truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def dev() -> int:
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = os.getenv("APP_PORT", "8080")
    use_local_db = _is_truthy(os.getenv("APP_DEV_USE_LOCAL_DB", "1"))
    if use_local_db:
        os.environ["DATABASE_URL"] = os.getenv("APP_DEV_DATABASE_URL", LOCAL_DEV_DATABASE_URL)
        print(f"Using local development database: {os.environ['DATABASE_URL']}")
    return _run(["uvicorn", "app.main:app", "--reload", "--host", host, "--port", port])


def start() -> int:
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = os.getenv("APP_PORT", "8080")
    return _run(["uvicorn", "app.main:app", "--host", host, "--port", port])


def test() -> int:
    return _run(["pytest", "-q"])


def test_verbose() -> int:
    return _run(["pytest", "-vv"])


def test_auth() -> int:
    return _run(["pytest", "-q", "tests/test_auth.py"])


def init_db() -> int:
    try:
        from app.database import init_db as _init_db

        _init_db()
        print("Database initialized.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print("Failed to initialize database.")
        print("Check DATABASE_URL and make sure the database is reachable.")
        print(f"Error: {exc}")
        return 1


def init_db_local() -> int:
    os.environ["DATABASE_URL"] = LOCAL_DEV_DATABASE_URL
    try:
        from app.database import init_db as _init_db

        _init_db()
        print("Local SQLite database initialized at ./app.db")
        return 0
    except Exception as exc:  # noqa: BLE001
        print("Failed to initialize local SQLite database.")
        print(f"Error: {exc}")
        return 1
