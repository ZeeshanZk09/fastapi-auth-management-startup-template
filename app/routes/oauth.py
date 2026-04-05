from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.controllers import oauth_controller
from app.utils.deps import get_session

router = APIRouter()


@router.get("/oauth/{provider}")
async def oauth_login(provider: str, request: Request):
    return await oauth_controller.handle_oauth_login(provider, request)


@router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: str,
    request: Request,
    db: Annotated[Session, Depends(get_session)],
):
    return await oauth_controller.handle_oauth_callback(provider, request, db)
