"""App settings, read from environment variables (see .env.example)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://egg:egg@db:5432/egg"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 12
    cors_origins: str = "http://localhost:5173"

    # First admin user, created by `python -m app.seed`
    first_admin_email: str = "admin@example.com"
    first_admin_password: str = "change-me-now"


@lru_cache
def get_settings() -> Settings:
    return Settings()
