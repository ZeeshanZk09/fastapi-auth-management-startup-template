from sqlmodel import Session, select
from app.models.user import User
from app.models.session import Session as UserSession
from fastapi import HTTPException
import uuid

USER_NOT_FOUND_DETAIL = "User not found"


def block_user(db: Session, user_id: uuid.UUID):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)
    user.is_blocked = True
    user.is_active = False
    db.add(user)
    revoke_all_user_sessions(db, user_id)
    db.commit()
    db.refresh(user)
    return user


def unblock_user(db: Session, user_id: uuid.UUID):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)
    user.is_blocked = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def activate_user(db: Session, user_id: uuid.UUID):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def inactivate_user(db: Session, user_id: uuid.UUID):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def revoke_all_user_sessions(db: Session, user_id: uuid.UUID):
    sessions = db.exec(select(UserSession).where(UserSession.user_id == user_id)).all()
    for session in sessions:
        session.revoked = True
        db.add(session)
    db.commit()
    return {"message": "All sessions revoked"}
