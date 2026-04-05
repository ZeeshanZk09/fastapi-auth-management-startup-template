# Project Audit (2026-04-05)

## Scope

- Run and fix the test suite using the existing `.venv`
- Remove PyMongo usage and migrate persistence to SQLModel
- Replace GitLab CI with GitHub Actions
- End with no test errors and no test warnings

## Key Findings and Fixes

- Import-time blocker in logging
  - Finding: `app/helper/log/logger.py` imported `pymongo` at module import time, causing test collection to fail when `pymongo` was missing.
  - Fix: Replaced Mongo sink implementation with SQLModel-backed persistence.

- Data layer lacked concrete DB implementation
  - Finding: `app/dal/connect.py` had a TODO only.
  - Fix: Added reusable SQLModel engine/session helpers and metadata initialization.

- CI configuration was GitLab-only
  - Finding: Project had only `.gitlab-ci.yml`.
  - Fix: Removed GitLab CI file and added `.github/workflows/ci.yml` for push/PR test automation.

- Dependency and tooling mismatch
  - Finding: `pyproject.toml` still pinned old package versions and `pymongo`, causing dependency conflicts and poor compatibility with current Python.
  - Fix: Updated dependency set to current compatible versions, removed `pymongo`, added `sqlmodel`, and aligned dev tooling versions.

- Warning noise in test runs
  - Finding: Deprecated `codecs.open` usage and brittle `version.txt` path triggered warnings.
  - Fix: Switched to built-in `open(..., encoding=...)` and made `version.txt` path deterministic from project root.

## Files Changed

- `app/dal/connect.py`
- `app/dal/data/__init__.py`
- `app/dal/data/log_record.py`
- `app/helper/log/logger.py`
- `app/configuration/configparser/wrapper.py`
- `app/configuration/getConfig.py`
- `tests/test_routers/test_routers.py`
- `pyproject.toml`
- `README.md`
- `.github/workflows/ci.yml`
- `.gitlab-ci.yml` (removed)

## Verification

Executed in `.venv`:

- `python -m pytest -q`

Result:

- `2 passed in 1.57s`
- No warnings emitted by pytest

## Current State

- Project imports cleanly with the updated dependency set
- Tests pass with no warnings
- SQLModel replaces previous Mongo-oriented logging persistence path
- CI runs on GitHub Actions instead of GitLab
