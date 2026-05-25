# tests/test_users_web_extra.py
# Este archivo contiene pruebas adicionales para la funcionalidad de gestión de
# usuarios en la interfaz web.


def fake_payload():
    return {
        "sub": "1",
        "email": "admin@test.com",
        "roles": ["admin"],
        "permissions": ["users:create", "users:read", "users:update", "users:delete"],
    }


def login_client(client):
    client.cookies.set("access_token", "fake")
    client.cookies.set("refresh_token", "fake")


def patch_auth(monkeypatch):
    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token",
        lambda token: fake_payload(),
    )


def test_update_user_roles_view(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.post(
        "/users/1/roles", data={"roles": [1]}, follow_redirects=False
    )
    assert response.status_code == 303


def test_deactivate_user(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.post("/users/1/deactivate", follow_redirects=False)
    assert response.status_code == 303


def test_activate_user(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.post("/users/1/activate", follow_redirects=False)
    assert response.status_code == 303


def test_delete_user_view(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.post("/users/2/delete", follow_redirects=False)
    assert response.status_code == 303
