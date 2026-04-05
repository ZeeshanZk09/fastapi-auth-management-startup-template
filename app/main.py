from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI

from app.database import init_db
from app.middlewares.auth_middleware import auth_middleware
from app.routes import admin, auth, oauth, users


def _read_app_version() -> str:
    version_path = Path(__file__).resolve().parents[1] / "version.txt"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
        return version or "0.0.0"
    except OSError:
        return "0.0.0"

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Python FastAPI Auth System",
    docs_url="/",
    version=_read_app_version(),
    lifespan=lifespan
)

# include the routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"], dependencies=[Depends(auth_middleware)])
app.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(auth_middleware)])
app.include_router(oauth.router, prefix="/auth", tags=["oauth"])
