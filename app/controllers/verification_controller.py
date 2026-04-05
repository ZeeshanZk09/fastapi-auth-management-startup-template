from sqlmodel import Session, select
from app.models.user import User
from app.utils.redis_client import redis_client
from fastapi import HTTPException


async def verify_email(db: Session, email: str, otp: str):
    stored_otp = await redis_client.get(f"email_otp:{email}")
    if not stored_otp or stored_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email_verified = True
    db.add(user)
    db.commit()
    await redis_client.delete(f"email_otp:{email}")
    return {"message": "Email verified successfully"}


async def verify_phone(db: Session, phone: str, otp: str):
    stored_otp = await redis_client.get(f"phone_otp:{phone}")
    if not stored_otp or stored_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user = db.exec(select(User).where(User.phone == phone)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.phone_verified = True
    db.add(user)
    db.commit()
    await redis_client.delete(f"phone_otp:{phone}")
    return {"message": "Phone verified successfully"}
