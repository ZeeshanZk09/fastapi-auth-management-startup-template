import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from app.models.enums import SessionStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Session(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    token: str = Field(unique=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=utc_now)
    revoked: bool = Field(default=False)
    status: SessionStatus = Field(default=SessionStatus.ACTIVE)
