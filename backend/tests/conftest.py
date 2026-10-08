import os

# Use a throwaway in-memory database for tests. Must be set before the app is imported.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["JWT_SECRET"] = "test-secret"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models.user import ROLE_ADMIN, ROLE_STAFF, User
from app.models.setting import DEFAULT_SETTINGS, AppSetting


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    session.add(User(email="admin@test.com", full_name="Admin", role=ROLE_ADMIN,
                     password_hash=hash_password("admin-pass")))
    session.add(User(email="staff@test.com", full_name="Staff", role=ROLE_STAFF,
                     password_hash=hash_password("staff-pass")))
    session.add(User(email="off@test.com", full_name="Off", role=ROLE_STAFF, is_active=False,
                     password_hash=hash_password("off-pass")))
    for k, v in DEFAULT_SETTINGS.items():
        session.add(AppSetting(key=k, value=v))
    session.commit()
    yield session
    session.close()


@pytest.fixture()
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


def login(client, email, password):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


@pytest.fixture()
def admin_headers(client):
    token = login(client, "admin@test.com", "admin-pass").json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
