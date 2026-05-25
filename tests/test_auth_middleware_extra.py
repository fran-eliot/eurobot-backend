# tests/test_auth_middleware_extra.py
# Este archivo contiene pruebas adicionales para la funcionalidad del middleware de
# autenticación. Se verifica que si tanto el token de acceso como el de refresh son
# inválidos, el usuario sea redirigido a la página de login.

from jose import JWTError


def test_middleware_redirect_when_refresh_invalid(client, monkeypatch):

    def fake_validate_access(token):
        raise JWTError("invalid access")

    def fake_validate_refresh(token):
        raise JWTError("invalid refresh")

    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token",
        fake_validate_access,
    )

    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_refresh_token",
        fake_validate_refresh,
    )

    client.cookies.set("access_token", "bad")
    client.cookies.set("refresh_token", "bad")

    response = client.get("/dashboard", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "/login"
