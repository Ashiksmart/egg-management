from datetime import datetime

from sqlalchemy import JSON, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AppSetting(Base):
    """One row per setting, e.g. key='eggs_per_petti', value=210."""

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    value: Mapped[object] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# Defaults only. They are copied into the table once by the seed script
# and can then be changed from the Settings page (Phase 2+).
DEFAULT_SETTINGS = {
    "eggs_per_petti": 210,
    "eggs_per_tray": 30,
    "wastage_target_percent": 1,
    "currency": "INR",
    "business_name": "My Egg Business",
    "invoice_prefix": "INV",
    "default_payment_terms_days": 0,
}
