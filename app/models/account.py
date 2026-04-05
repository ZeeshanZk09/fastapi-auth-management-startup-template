import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Account(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    provider: str
    provider_user_id: str
    access_token: str  # Should be encrypted
    created_at: datetime = Field(default_factory=utc_now)
