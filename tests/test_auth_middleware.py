# tests/test_auth_middleware.py
# Este archivo contiene pruebas para el middleware de autenticación de la aplicación.

from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import JWTError

from app.core.middleware.auth_middleware import AuthMiddleware


def make_app():
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    @app.get("/private")
    async def private():
        return {"ok": True}

    @app.get("/login")
    async def login():
        return {"login": True}

    @app.get("/api/test")
    async def api():
        return {"api": True}

    return app


def test_public_path_login():
    client = TestClient(make_app())
    r = client.get("/login")
    assert r.status_code == 200


def test_api_bypass():
    client = TestClient(make_app())
    r = client.get("/api/test")
    assert r.status_code == 200


def test_private_without_token():
    client = TestClient(make_app())
    r = client.get("/private", follow_redirects=False)
    assert r.status_code == 302


def test_private_invalid_token(monkeypatch):

    def fake_validate(token):
        raise JWTError("bad token")

    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token", fake_validate
    )

    client = TestClient(make_app())

    client.cookies.set("access_token", "bad")
    r = client.get("/private", follow_redirects=False)

    assert r.status_code == 302
