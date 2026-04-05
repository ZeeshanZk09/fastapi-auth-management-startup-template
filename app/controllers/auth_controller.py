import random
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.auth import UserCreate
from app.utils.password import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from app.utils.email import send_verification_email
from app.utils.sms import send_sms_otp
from app.models.session import Session as UserSession
from app.utils.exceptions import inactive_user_exception, blocked_user_exception


async def register_user(db: Session, user_create: UserCreate, redis_client: Redis):
    existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        user_name=user_create.user_name,
        email=user_create.email,
        phone=user_create.phone,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    await send_verification_otp(db_user.email, db_user.phone, redis_client)
    return db_user


def login_user(db: Session, form_data):
    user = db.exec(select(User).where(User.user_name == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.is_active:
        raise inactive_user_exception
    if user.is_blocked:
        raise blocked_user_exception

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )

    session = UserSession(
        user_id=user.id,
        token=access_token,
        expires_at=datetime.now(timezone.utc) + access_token_expires,
    )
    db.add(session)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer", "user": user}


async def send_verification_otp(email: str, phone: str, redis_client):
    email_otp = str(random.randint(100000, 999999))
    phone_otp = str(random.randint(100000, 999999))
    await redis_client.set(f"email_otp:{email}", email_otp, ex=600)
    await redis_client.set(f"phone_otp:{phone}", phone_otp, ex=600)
    await send_verification_email(email, email_otp)
    await send_sms_otp(phone, phone_otp)


def get_user_by_token(db: Session, token: str):
    session = db.exec(select(UserSession).where(UserSession.token == token)).first()
    if not session or session.revoked or session.expires_at < datetime.now(timezone.utc):
        return None
    return db.get(User, session.user_id)
