import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.utils.deps import get_session
from app.config import settings
from app.schemas.auth import UserCreate
from app.controllers.auth_controller import register_user
from app.utils.redis_client import get_redis_client
from unittest.mock import AsyncMock
import asyncio
import redis

DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_db_override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_db_override

def get_redis_override():
    return AsyncMock()

app.dependency_overrides[get_redis_client] = get_redis_override


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_register(client: TestClient, session: Session):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "user_name": "testuser",
            "email": "test@example.com",
            "phone": "1234567890",
            "password": "password",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.anyio
async def test_login(client: TestClient, session: Session):
    user_create = UserCreate(
        first_name="Test",
        last_name="User",
        user_name="testuser",
        email="test@example.com",
        phone="1234567890",
        password="password",
    )
    redis_client_mock = AsyncMock()
    await register_user(session, user_create, redis_client_mock)

    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
