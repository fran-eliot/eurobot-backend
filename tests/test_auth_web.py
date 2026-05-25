# tests/test_auth_web.py
# Este archivo contiene pruebas para la funcionalidad de autenticación web.
# Se definen pruebas para verificar que las rutas de autenticación funcionan
# correctamente, incluyendo el inicio de sesión, la actualización de tokens y
# el cierre de sesión.

from fastapi import HTTPException


# -------------------------------------------------
# GET /login
# -------------------------------------------------
def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


# -------------------------------------------------
# POST /login OK
# -------------------------------------------------
def test_login_ok(client, monkeypatch):
    class FakeUser:
        id_usuario = 1

    def fake_authenticate(db, email, password):
        return {
            "access_token": "access123",
            "refresh_token": "refresh123",
            "user": FakeUser(),
        }

    monkeypatch.setattr("app.web.auth_web.authenticate_user", fake_authenticate)

    response = client.post(
        "/login",
        data={"email": "admin@test.com", "password": "1234"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/dashboard"

    cookies = response.headers.get("set-cookie", "")
    assert "access_token=access123" in cookies
    assert "refresh_token=refresh123" in cookies


# -------------------------------------------------
# POST /login FAIL
# -------------------------------------------------
def test_login_fail(client, monkeypatch):
    def fake_authenticate(db, email, password):
        raise HTTPException(status_code=401)

    monkeypatch.setattr("app.web.auth_web.authenticate_user", fake_authenticate)

    response = client.post(
        "/login", data={"email": "bad@test.com", "password": "wrong"}
    )

    assert response.status_code == 200
    assert "Credenciales incorrectas" in response.text


# -------------------------------------------------
# GET /refresh OK
# -------------------------------------------------
def test_refresh_ok(client, monkeypatch):
    client.cookies.set("refresh_token", "goodtoken")

    monkeypatch.setattr(
        "app.web.auth_web.validate_refresh_token",
        lambda token: {"sub": "1", "type": "refresh"},
    )

    monkeypatch.setattr(
        "app.web.auth_web.refresh_access_token", lambda payload, request: "new_access"
    )

    response = client.get("/refresh", follow_redirects=False)

    assert response.status_code in (302, 307)
    cookies = response.headers.get("set-cookie", "")
    assert "access_token=new_access" in cookies


# -------------------------------------------------
# GET /refresh FAIL no cookie
# -------------------------------------------------
def test_refresh_no_cookie(client):
    client.cookies.clear()

    response = client.get("/refresh")

    assert response.status_code == 401


# -------------------------------------------------
# POST /logout
# -------------------------------------------------
def test_logout(client):
    response = client.post("/logout", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"
