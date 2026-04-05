from fastapi import Request
from app.models.enums import Role
from app.utils.exceptions import admin_required_exception


def admin_middleware(request: Request):
    user = request.state.user
    if user.role != Role.ADMIN:
        raise admin_required_exception
