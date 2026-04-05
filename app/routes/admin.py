from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.controllers import admin_controller, user_controller
from app.utils.deps import get_session
from app.middlewares.admin_middleware import admin_middleware
import uuid
from typing import Annotated, List
from app.schemas.user import User

router = APIRouter(dependencies=[Depends(admin_middleware)])


@router.get("/users", response_model=List[User])
async def read_users(db: Annotated[Session, Depends(get_session)], skip: int = 0, limit: int = 100):
    return user_controller.get_all_users(db, skip, limit)


@router.patch("/users/{user_id}/block")
async def block_user_route(user_id: uuid.UUID, db: Annotated[Session, Depends(get_session)]):
    return admin_controller.block_user(db, user_id)


@router.patch("/users/{user_id}/unblock")
async def unblock_user_route(user_id: uuid.UUID, db: Annotated[Session, Depends(get_session)]):
    return admin_controller.unblock_user(db, user_id)


@router.patch("/users/{user_id}/activate")
async def activate_user_route(user_id: uuid.UUID, db: Annotated[Session, Depends(get_session)]):
    return admin_controller.activate_user(db, user_id)


@router.patch("/users/{user_id}/inactivate")
async def inactivate_user_route(user_id: uuid.UUID, db: Annotated[Session, Depends(get_session)]):
    return admin_controller.inactivate_user(db, user_id)


@router.delete("/users/{user_id}/sessions")
async def revoke_sessions_route(user_id: uuid.UUID, db: Annotated[Session, Depends(get_session)]):
    return admin_controller.revoke_all_user_sessions(db, user_id)


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: uuid.UUID, db: Annotated[Session, Depends(get_session)]):
    return user_controller.get_user_by_id(db, user_id)
