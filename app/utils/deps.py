from typing import Annotated, Generator

from fastapi import Depends
from redis.asyncio import Redis
from sqlmodel import Session

from app.controllers.auth_controller import get_user_by_token
from app.database import get_session as get_db_session
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.utils.exceptions import credentials_exception
from app.utils.redis_client import redis_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_session() -> Generator[Session, None, None]:
    yield from get_db_session()


def get_redis() -> Redis:
    return redis_client


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_session)],
) -> User:
    user = get_user_by_token(db, token)
    if not user:
        raise credentials_exception
    return user
