from tests.test_utils import login_admin

# =========================================================
# LISTADO - FILTROS Y PAGINACIÓN
# =========================================================


def test_identities_list_search(client):
    login_admin(client)

    response = client.get("/identities/?search=admin1")

    assert response.status_code == 200
    assert "admin1@robotica.es" in response.text


def test_identities_list_provider_filter_local(client):
    login_admin(client)

    response = client.get("/identities/?provider=local")

    assert response.status_code == 200


def test_identities_list_provider_filter_saml(client):
    login_admin(client)

    response = client.get("/identities/?provider=uah_saml")

    assert response.status_code == 200
    assert "user_uah@uah.es" in response.text


def test_identities_list_page_2(client):
    login_admin(client)

    response = client.get("/identities/?page=2")

    assert response.status_code == 200


# =========================================================
# FORMULARIOS
# =========================================================


def test_identity_form_create(client):
    login_admin(client)

    response = client.get("/identities/form")

    assert response.status_code == 200
    assert "email" in response.text.lower()


def test_identity_form_edit(client):
    login_admin(client)

    response = client.get("/identities/2/edit")

    assert response.status_code == 200
    assert "admin1@robotica.es" in response.text


# =========================================================
# DETAIL
# =========================================================


def test_identity_detail_ok(client):
    login_admin(client)

    response = client.get("/identities/2")

    assert response.status_code == 200
    assert "admin1@robotica.es" in response.text


def test_identity_detail_404(client):
    login_admin(client)

    response = client.get("/identities/999")

    assert response.status_code == 404


# =========================================================
# UPDATE CON PASSWORD NUEVA
# =========================================================


def test_identity_edit_with_password(client):
    login_admin(client)

    response = client.post(
        "/identities/2/edit",
        data={
            "email": "admin1_updated@robotica.es",
            "password": "nueva1234",
            "user_id": 1,
        },
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/identities/"


# =========================================================
# DELETE NO EXISTE
# =========================================================


def test_identity_delete_not_found(client):
    login_admin(client)

    response = client.post("/identities/999/delete", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert response.headers["location"] == "/identities/"
