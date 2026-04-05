from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    phone: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


class VerifyEmail(BaseModel):
    email: EmailStr
    otp: str


class VerifyPhone(BaseModel):
    phone: str
    otp: str
