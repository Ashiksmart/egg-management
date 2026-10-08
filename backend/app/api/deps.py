"""Shared route dependencies: who is logged in, and role checks."""
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import decode_access_token
from app.models.user import ROLE_ADMIN, User

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if creds is None:
        raise AppError("NOT_AUTHENTICATED", "Please log in.", 401)
    try:
        payload = decode_access_token(creds.credentials)
    except jwt.PyJWTError:
        raise AppError("INVALID_TOKEN", "Login expired. Please log in again.", 401)
    user = db.get(User, int(payload["sub"]))
    if user is None or not user.is_active:
        raise AppError("INVALID_USER", "User not found or disabled.", 401)
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != ROLE_ADMIN:
        raise AppError("FORBIDDEN", "Admin access required.", 403)
    return user
