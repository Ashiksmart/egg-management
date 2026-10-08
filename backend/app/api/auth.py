from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenOut, UserOut
from app.schemas.common import ok

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    print("Data 1111")
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    print("Data 2222")

    # Same message for wrong email and wrong password, so nobody can guess emails.
    if user is None or not user.is_active or not verify_password(body.password, user.password_hash):
        raise AppError("BAD_CREDENTIALS", "Wrong email or password.", 401)
    token = create_access_token(user.id, user.role)
    out = TokenOut(access_token=token, user=UserOut.model_validate(user))
    return ok(out.model_dump())


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return ok(UserOut.model_validate(user).model_dump())
