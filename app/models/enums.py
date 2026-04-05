from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class SessionStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
