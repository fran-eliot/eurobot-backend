# test/test_permissions.py
# Este archivo contiene pruebas para verificar que los permisos de acceso a las rutas
# de la aplicación funcionan correctamente. Se prueban diferentes escenarios de
# acceso para usuarios con distintos roles y permisos.


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=False
    )


def test_admin_can_access_users(client):
    login(client, "admin1@robotica.es", "1234")

    response = client.get("/users/")
    assert response.status_code == 200


def test_student_can_access_dashboard(client):
    login(client, "alumno1@uah.es", "1234")

    response = client.get("/dashboard")
    assert response.status_code == 200


def test_student_cannot_access_roles(client):
    login(client, "alumno1@uah.es", "1234")

    response = client.get("/roles/")
    assert response.status_code in (403, 401)


def test_uah_user_can_access_dashboard(client):
    client.get("/auth/saml/mock", follow_redirects=False)

    dashboard = client.get("/dashboard")
    assert dashboard.status_code == 200
