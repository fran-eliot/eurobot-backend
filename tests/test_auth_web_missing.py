# tests/test_auth_web_missing.py
# Este archivo contiene pruebas para la funcionalidad de autenticación web.


def test_refresh_invalid_token(client):
    client.cookies.set("refresh_token", "bad-token")

    response = client.get("/refresh", follow_redirects=False)

    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token inválido"


def test_logout_with_authenticated_user(client, monkeypatch):
    def fake_validate(token):
        return {
            "sub": "1",
            "email": "admin@test.com",
            "roles": ["admin"],
            "permissions": [],
        }

    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token", fake_validate
    )

    client.cookies.set("access_token", "fake")
    client.cookies.set("refresh_token", "fake")

    response = client.post("/logout", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"
