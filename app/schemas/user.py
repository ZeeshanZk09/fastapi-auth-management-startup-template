from pydantic import BaseModel, EmailStr, ConfigDict
import uuid
from datetime import datetime
from app.models.enums import Role


class UserBase(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    phone: str


class User(UserBase):
    id: uuid.UUID
    email_verified: bool
    phone_verified: bool
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_blocked: bool
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    user_name: str | None = None
