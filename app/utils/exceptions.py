from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

inactive_user_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Inactive user",
)

blocked_user_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is blocked",
)

not_verified_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Verify email and phone first",
)

admin_required_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Admin privileges required",
)
