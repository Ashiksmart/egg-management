"""Creates the first admin user and default settings. Safe to run many times.

Run:  python -m app.seed
"""
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.setting import DEFAULT_SETTINGS, AppSetting
from app.models.user import ROLE_ADMIN, User


def seed(db) -> None:
    s = get_settings()
    email = s.first_admin_email.lower()
    if db.scalar(select(User).where(User.email == email)) is None:
        db.add(
            User(
                email=email,
                full_name="Admin",
                password_hash=hash_password(s.first_admin_password),
                role=ROLE_ADMIN,
            )
        )
    for key, value in DEFAULT_SETTINGS.items():
        if db.scalar(select(AppSetting).where(AppSetting.key == key)) is None:
            db.add(AppSetting(key=key, value=value))
    db.commit()


if __name__ == "__main__":
    with SessionLocal() as session:
        seed(session)
    print("Seed done.")
