from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserUpdate
from fastapi import HTTPException
import uuid


def get_user_profile(_db: Session, user: User):
    return user


def update_user_profile(db: Session, user: User, user_update: UserUpdate):
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(User).offset(skip).limit(limit)).all()


def get_user_by_id(db: Session, user_id: uuid.UUID):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
