# Python [Fastapi](https://fastapi.tiangolo.com/) Template Project with [poetry](https://python-poetry.org/) and [Docker](https://www.docker.com/101-tutorial)

## Used frameworks/technologies

- [Fastapi](https://fastapi.tiangolo.com/tutorial/)
- [Fastapi & Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/101-tutorial)
- [Helm](https://opensource.com/article/20/5/helm-charts)

## How to use the template

1. Clone the template (Or use the "Use this template" button in GitHub directly!)
   - `git clone https://github.com/Salfiii/fastapi-template.git`
2. remove the ".git"-Folder from the local repository to delete the reference to the template project
3. create a new git repository locally
4. (install [poetry](https://python-poetry.org/docs/) if you want to run it locally)
5. Install [Docker](https://www.docker.com/products/docker-desktop/) or use a remote machine if you have one
6. change the project name from "fastapi-template" to something to your likings (you can also run it directly, if you like so)
   - in the parent Folder "fastapi-template"
   - in the [pyproject.toml](pyproject.toml)
   - in the [main.py](app/main.py)
   - in the [dockerfile](Dockerfile)
7. Run the dockerfile (you can change "fastapi-template" to whatever you like):
   - `docker build -t fastapi-template . && docker run -it -p 50001:8080 fastapi-template`
   - If you want to remove the dockerfile after exiting the service automatically, add "--rm" before "-it"
   - You can change the port 50001 to whatever port you want to use on your host
8. Open <http://localhost:50001> in your browser and you should see the OpenAPI docs.

## Documentation

### Poetry helper commands

After running `poetry install`, you can use these convenience commands:

- `poetry run app-dev` -> start FastAPI with auto-reload
- `poetry run app-start` -> start FastAPI without reload
- `poetry run app-test` -> run all tests quickly (`pytest -q`)
- `poetry run app-test-v` -> run tests in verbose mode
- `poetry run app-test-auth` -> run only auth tests
- `poetry run app-init-db` -> initialize tables using the configured `DATABASE_URL`
- `poetry run app-init-db-local` -> initialize local SQLite database at `./app.db`

`app-dev` defaults to local SQLite (`sqlite:///./app.db`) to avoid startup failures when Postgres is not configured.
If you want to use your configured `DATABASE_URL` in development, run:

- PowerShell: `$env:APP_DEV_USE_LOCAL_DB="0"; poetry run app-dev`

### File structure

#### [app](app)

Contains the general python application.

- **[config.py](app/config.py)**:
  - Environment-driven application settings loaded via `pydantic-settings`.
- **[database.py](app/database.py)**:
  - SQLModel engine/session helpers and table bootstrap.
- **[routes](app/routes)**:
  - HTTP route modules for `auth`, `users`, `admin`, and `oauth`.
- **[controllers](app/controllers)**:
  - Request/business logic handlers for each route domain.
- **[models](app/models)**:
  - SQLModel ORM entities (`user`, `session`, `account`).
- **[utils](app/utils)**:
  - Shared helpers (JWT, dependencies, email, SMS, redis client).
- **[gunicorn_conf.py](app/gunicorn_conf.py)**:
  - Gunicorn runtime configuration.
- **[main.py](app/main.py)**:
  - FastAPI app entry point and router registration.

#### [docs](docs)

Local location for documentation

#### [Helm](helm)

Application environment-specific Helm values.
Contains files that define deployment values for `test`, `kons`, and `prod`.

- [test_values.yaml](helm/test_values.yaml): Test environment -> **This file includes an explanation of the different options**
- [Kons_values.yaml](helm/kons_values.yaml): Consolidation environment
- [Prod_values.yaml](helm/prod_values.yaml): Production environment

#### [tests](tests)

- Location for the tests which are created with the [pytest framework](https://docs.pytest.org/en/6.2.x/).
- Documentation for the creation of [tests for Fastapi](https://fastapi.tiangolo.com/tutorial/testing/)
- To carry out the tests: Right-click on the test folder -> "Run 'Pytests' in tests"
- Main test module in this template: [test_auth.py](tests/test_auth.py)

#### [tmp] (tmp)

- [in](tmp/in): used for temporary input file storage.
- [out](tmp/out): used for temporary output file storage.
- [test](tmp/test): can be used to keep scripts to try things out.

#### Additional files

- [Dockerfile](./Dockerfile): Docker file that orchestrates the creation of the Docker container.
- [version.txt](version.txt): Current version of the application shown in OpenAPI docs.
- [.github/workflows/ci.yml](.github/workflows/ci.yml): GitHub Actions workflow for test automation.
- [README.md](README.md): Project documentation.
- [.gitignore](.gitignore): Files and folders excluded from git versioning.
- [pyproject.toml](pyproject.toml): [Poetry project file](https://python-poetry.org/docs/pyproject/).
