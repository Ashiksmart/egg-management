from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.setting import AppSetting
from app.models.user import User
from app.schemas.common import ok

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def list_settings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.scalars(select(AppSetting).order_by(AppSetting.key)).all()
    return ok({r.key: r.value for r in rows})
