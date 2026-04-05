from pydantic import BaseModel
import uuid


class UserBlock(BaseModel):
    user_id: uuid.UUID
