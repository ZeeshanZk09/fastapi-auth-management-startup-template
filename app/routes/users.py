from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.user import User as UserSchema, UserUpdate
from app.models.user import User as UserModel
from app.controllers import user_controller
from app.utils.deps import get_session, get_current_user
from app.middlewares.verification_middleware import verification_middleware

router = APIRouter()


@router.get("/me", response_model=UserSchema, dependencies=[Depends(verification_middleware)])
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    return user_controller.get_user_profile(db, current_user)


@router.patch("/me", response_model=UserSchema, dependencies=[Depends(verification_middleware)])
async def update_user_me(
    user_update: UserUpdate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
):
    return user_controller.update_user_profile(db, current_user, user_update)
