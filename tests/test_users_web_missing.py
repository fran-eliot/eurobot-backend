# tests/test_users_web_missing.py
# Este archivo contiene pruebas para la funcionalidad de gestión de usuarios en la
# interfaz web.


def fake_payload():
    return {
        "sub": "1",
        "email": "admin@test.com",
        "roles": ["admin"],
        "permissions": [
            "users:create",
            "users:read",
            "users:update",
            "users:delete",
        ],
    }


def login_client(client):
    client.cookies.set("access_token", "fake")
    client.cookies.set("refresh_token", "fake")


def patch_auth(monkeypatch):
    monkeypatch.setattr(
        "app.core.middleware.auth_middleware.validate_access_token",
        lambda token: fake_payload(),
    )


# -------------------------------------------------
# CREATE -> ValidationError branch
# -------------------------------------------------
def test_user_create_validation_error(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.post(
        "/users/form",
        data={"nombre": "   ", "activo": True},
        follow_redirects=False,
    )
    assert response.status_code == 200


# -------------------------------------------------
# UPDATE -> ValidationError branch
# -------------------------------------------------
def test_user_update_validation_error(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.post(
        "/users/1/edit",
        data={"nombre": "   ", "activo": True},
        follow_redirects=False,
    )
    assert response.status_code == 200


# -------------------------------------------------
# LIST with params
# -------------------------------------------------
def test_users_list_filtered(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.get("/users/?search=admin&status=active&page=1")
    assert response.status_code == 200


# -------------------------------------------------
# EDIT FORM
# -------------------------------------------------
def test_user_edit_form(client, monkeypatch):
    patch_auth(monkeypatch)
    login_client(client)

    response = client.get("/users/1/edit")
    assert response.status_code == 200
