import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.enums import Role, UserStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str
    last_name: str
    user_name: str = Field(unique=True)
    email: str = Field(unique=True, index=True)
    phone: str = Field(unique=True, index=True)
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now, sa_column_kwargs={"onupdate": utc_now})
    hashed_password: Optional[str] = Field(nullable=True)
    is_active: bool = Field(default=True)
    is_blocked: bool = Field(default=False)
    role: Role = Field(default=Role.USER)
