from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlmodel import Session
import random
from app.schemas.auth import UserCreate, UserLogin, ForgotPassword, ResetPassword, VerifyEmail, VerifyPhone
from app.controllers import auth_controller, verification_controller
from app.utils.deps import get_session
from app.utils.password import get_password_hash
from app.utils.redis_client import get_redis_client
from app.utils.email import send_password_reset_email
from app.models.user import User
from sqlmodel import select

router = APIRouter()


@router.post("/register")
async def register(
    user: UserCreate,
    db: Annotated[Session, Depends(get_session)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    return await auth_controller.register_user(db, user, redis_client)


@router.post("/login")
async def login(form_data: UserLogin, db: Annotated[Session, Depends(get_session)]):
    return auth_controller.login_user(db, form_data)


@router.post(
    "/forgot-password",
    responses={404: {"description": "User not found"}},
)
async def forgot_password(
    data: ForgotPassword,
    db: Annotated[Session, Depends(get_session)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = str(random.randint(100000, 999999))
    await redis_client.set(f"reset_otp:{data.email}", otp, ex=600)
    await send_password_reset_email(data.email, otp)
    return {"message": "Password reset OTP sent"}


@router.post(
    "/reset-password",
    responses={
        400: {"description": "Invalid OTP"},
        404: {"description": "User not found"},
    },
)
async def reset_password(
    data: ResetPassword,
    db: Annotated[Session, Depends(get_session)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    stored_otp = await redis_client.get(f"reset_otp:{data.email}")
    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(data.new_password)
    db.add(user)
    db.commit()
    await redis_client.delete(f"reset_otp:{data.email}")
    return {"message": "Password reset successfully"}


@router.post("/verify-email")
async def verify_email_route(data: VerifyEmail, db: Annotated[Session, Depends(get_session)]):
    return await verification_controller.verify_email(db, data.email, data.otp)


@router.post("/verify-phone")
async def verify_phone_route(data: VerifyPhone, db: Annotated[Session, Depends(get_session)]):
    return await verification_controller.verify_phone(db, data.phone, data.otp)
