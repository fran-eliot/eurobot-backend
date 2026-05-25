# tests/test_identities_crud.py

from tests.test_utils import login_admin, login_student


def test_identities_list(client):
    login_admin(client)

    response = client.get("/identities/")
    assert response.status_code == 200


def test_create_identity(client):
    login_admin(client)

    response = client.post(
        "/identities/form",
        data={"email": "nuevo@robotica.es", "password": "1234", "user_id": 1},
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/identities/"


def test_edit_identity(client):
    login_admin(client)

    # Crear primero
    create = client.post(
        "/identities/form",
        data={"email": "editar@robotica.es", "password": "1234", "user_id": 1},
        follow_redirects=False,
    )

    assert create.status_code in (302, 303)

    # Buscar detalle en listado por id conocido reciente
    response = client.get("/identities/")
    assert response.status_code == 200

    # En tus seeds ya existen ids 1,2,3 -> nuevo suele ser 4+
    identity_id = 4

    update = client.post(
        f"/identities/{identity_id}/edit",
        data={"email": "editado@robotica.es", "password": "", "user_id": 1},
        follow_redirects=False,
    )

    assert update.status_code in (302, 303)


def test_delete_identity(client):
    login_admin(client)

    # Crear identity a borrar
    client.post(
        "/identities/form",
        data={"email": "borrar@robotica.es", "password": "1234", "user_id": 1},
        follow_redirects=False,
    )

    identity_id = 4

    response = client.post(f"/identities/{identity_id}/delete", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/identities/"


def test_duplicate_email_identity(client):
    login_admin(client)

    response = client.post(
        "/identities/form",
        data={
            "email": "admin1@robotica.es",  # ya existe en seed
            "password": "1234",
            "user_id": 1,
        },
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)


def test_student_cannot_access_identities(client):
    login_student(client)

    response = client.get("/identities/", follow_redirects=False)
    assert response.status_code in (302, 403)
