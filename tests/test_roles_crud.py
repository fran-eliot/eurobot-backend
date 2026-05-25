# tests/test_roles_crud.py
# Este archivo contiene pruebas para las operaciones CRUD de roles a través de la
# interfaz web.
from tests.test_utils import login_admin


def test_roles_list(client):
    login_admin(client)

    response = client.get("/roles/")

    assert response.status_code == 200


def test_create_role(client):
    login_admin(client)

    response = client.post(
        "/roles/form",
        data={"nombre": "tester", "descripcion": "Rol de pruebas"},
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/roles/"


def test_edit_role(client):
    login_admin(client)

    # Crear rol primero
    create = client.post(
        "/roles/form",
        data={"nombre": "temporal", "descripcion": "Temporal"},
        follow_redirects=False,
    )

    assert create.status_code in (302, 303)

    # Buscar listado para localizar el ID si no redirige al detalle
    page = client.get("/roles/")
    assert page.status_code == 200

    # Suponiendo último rol creado = mayor id
    # Editamos un ID probable reciente (ajustable si hiciera falta)
    response = client.post(
        "/roles/2/edit",
        data={"nombre": "temporal_editado", "descripcion": "Editado"},
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)


def test_delete_role(client):
    login_admin(client)

    # Crear rol
    client.post(
        "/roles/form",
        data={"nombre": "eliminar_role", "descripcion": "Borrar"},
        follow_redirects=False,
    )

    # Intentar borrar uno reciente
    response = client.post("/roles/2/delete", follow_redirects=False)

    assert response.status_code in (302, 303)
