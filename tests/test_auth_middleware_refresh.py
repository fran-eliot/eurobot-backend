# tests/test_auth_middleware_refresh.py
# Este archivo contiene pruebas para la funcionalidad de refresco de tokens en el
# middleware de autenticación de la aplicación. Se verifica que el middleware pueda
# manejar correctamente el caso en el que el token de acceso es inválido pero el
# token de refresco es válido, y que se genere un nuevo token de acceso y se permita
# el acceso a la ruta protegida.

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from jose import JWTError
from starlette.testclient import TestClient

from app.core.middleware.auth_middleware import AuthMiddleware


def test_refresh_token_success(monkeypatch):
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    @app.get("/private")
    async def private():
        return PlainTextResponse("ok")

    # access inválido
    def fake_validate_access(token):
        raise JWTError()

    # refresh válido
    def fake_validate_refresh(token):
        return {"sub": "1", "type": "refresh"}

    # genera nuevo token
    def fake_refresh_access_token(payload, db):
        return "new_access"

    # validar nuevo access
    def fake_validate_new(token):
        if token == "new_access":
            return {"sub": "1"}
        raise JWTError()

    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token",
        fake_validate_access,
    )
    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_refresh_token",
        fake_validate_refresh,
    )
    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.refresh_access_token",
        fake_refresh_access_token,
    )

    # segunda llamada para nuevo token
    calls = {"n": 0}

    def wrapper(token):
        calls["n"] += 1
        if calls["n"] == 1:
            raise JWTError()
        return {"sub": "1"}

    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token", wrapper
    )

    client = TestClient(app)
    client.cookies.set("access_token", "bad")
    client.cookies.set("refresh_token", "good")
    response = client.get("/private")

    assert response.status_code == 200
    assert response.text == "ok"
