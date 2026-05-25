# tests/test_roles_web_extra.py
# Este archivo contiene pruebas adicionales para la funcionalidad web de roles.
# Se prueban casos como la visualización de formularios, la creación y edición
# de roles, la eliminación de roles y la protección de rutas que requieren
# autenticación.

from tests.test_utils import login_admin

# =====================================================
# ROLES WEB EXTRA
# =====================================================


def test_role_form_create(client):
    login_admin(client)

    response = client.get("/roles/form")

    assert response.status_code == 200


def test_role_form_edit(client):
    login_admin(client)

    response = client.get("/roles/1/edit")

    assert response.status_code == 200


def test_role_detail_view(client):
    login_admin(client)

    response = client.get("/roles/1")

    assert response.status_code == 200


def test_role_create_ok(client):
    login_admin(client)

    response = client.post(
        "/roles/form",
        data={
            "nombre": "teacher",
            "descripcion": "Rol profesor",
            "permissions": [1, 2],
        },
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/roles/"


def test_role_edit_ok(client):
    login_admin(client)

    # crear uno nuevo primero
    client.post(
        "/roles/form",
        data={"nombre": "temp_role", "descripcion": "Temporal"},
        follow_redirects=False,
    )

    response = client.post(
        "/roles/2/edit",
        data={
            "nombre": "temp_editado",
            "descripcion": "Actualizado",
            "permissions": [1, 2, 3],
        },
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)


def test_role_delete_ok(client):
    login_admin(client)

    client.post(
        "/roles/form",
        data={"nombre": "borrar_role", "descripcion": "Eliminar"},
        follow_redirects=False,
    )

    response = client.post("/roles/2/delete", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/roles/"


# =====================================================
# ERRORES / EXCEPT
# =====================================================


def test_role_create_duplicate_name(client):
    login_admin(client)

    response = client.post(
        "/roles/form", data={"nombre": "admin", "descripcion": "Duplicado"}
    )

    assert response.status_code == 200


def test_role_edit_duplicate_name(client):
    login_admin(client)

    response = client.post(
        "/roles/2/edit", data={"nombre": "admin", "descripcion": "Duplicado"}
    )

    assert response.status_code == 200
