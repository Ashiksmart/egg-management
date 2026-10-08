from tests.conftest import login


def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "up"


def test_login_success_returns_token_and_user(client):
    r = login(client, "admin@test.com", "admin-pass")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["access_token"]
    assert data["user"]["role"] == "ADMIN"
    assert "password" not in str(data)


def test_login_wrong_password(client):
    r = login(client, "admin@test.com", "nope")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "BAD_CREDENTIALS"


def test_login_unknown_email_same_error(client):
    r = login(client, "ghost@test.com", "x")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "BAD_CREDENTIALS"


def test_login_disabled_user_rejected(client):
    r = login(client, "off@test.com", "off-pass")
    assert r.status_code == 401


def test_login_bad_email_format_is_validation_error(client):
    r = login(client, "not-an-email", "x")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"


def test_me_requires_token(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401


def test_me_with_token(client, admin_headers):
    r = client.get("/api/v1/auth/me", headers=admin_headers)
    assert r.status_code == 200
    assert r.json()["data"]["email"] == "admin@test.com"


def test_bad_token_rejected(client):
    r = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer garbage"})
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "INVALID_TOKEN"


def test_settings_defaults_visible_to_logged_in_user(client, admin_headers):
    r = client.get("/api/v1/settings", headers=admin_headers)
    data = r.json()["data"]
    assert data["eggs_per_petti"] == 210
    assert data["eggs_per_tray"] == 30


def test_settings_need_login(client):
    assert client.get("/api/v1/settings").status_code == 401
