# tests/test_users_crud.py
# Este archivo contiene pruebas para verificar que las operaciones CRUD de usuarios
# funcionan correctamente. Se prueban la creación, edición y eliminación de usuarios,
# así como la visualización de la lista de usuarios. Para realizar estas  pruebas,
# se utiliza un cliente de prueba de FastAPI para simular solicitudes a la aplicación
# y verificar las respuestas.

from tests.test_utils import login_admin


def test_users_list(client):
    login_admin(client)

    response = client.get("/users/")
    assert response.status_code == 200
    assert "Admin Principal" in response.text


def test_create_user(client):
    login_admin(client)

    response = client.post(
        "/users/form",
        data={"nombre": "Usuario Test", "activo": "on"},
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)


def test_edit_user(client):
    login_admin(client)

    create = client.post(
        "/users/form",
        data={"nombre": "Temporal", "activo": "on"},
        follow_redirects=False,
    )

    location = create.headers["location"]  # /users/27
    user_id = location.split("/")[-1]

    response = client.post(
        f"/users/{user_id}/edit",
        data={"nombre": "Temporal Editado", "activo": "on"},
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)


def test_delete_user(client):
    login_admin(client)

    create = client.post(
        "/users/form",
        data={"nombre": "Eliminar Test", "activo": "on"},
        follow_redirects=False,
    )

    location = create.headers["location"]
    user_id = location.split("/")[-1]

    response = client.post(f"/users/{user_id}/delete", follow_redirects=False)

    assert response.status_code in (302, 303)
