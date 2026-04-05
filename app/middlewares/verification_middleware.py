from fastapi import Request
from app.utils.exceptions import not_verified_exception


def verification_middleware(request: Request):
    user = request.state.user
    if not user.email_verified or not user.phone_verified:
        raise not_verified_exception
