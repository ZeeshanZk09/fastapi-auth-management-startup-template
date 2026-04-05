from fastapi import Request, Depends
from app.utils.deps import get_current_user
from app.models.user import User


def auth_middleware(request: Request, user: User = Depends(get_current_user)):
    request.state.user = user
