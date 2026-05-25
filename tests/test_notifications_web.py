# tests/test_notifications_web.py


from tests.test_utils import login_admin


def test_notifications_page(client):
    login_admin(client)

    response = client.get("/notifications/")

    assert response.status_code == 200


def test_read_notification_success(client, db):
    from app.modules.notifications.notification_constants import NotificationType
    from app.modules.notifications.notification_service import create_notification
    from app.modules.users.user_model import User

    login_admin(client)

    admin = db.query(User).filter_by(nombre="Admin Principal").first()

    notification = create_notification(
        db=db,
        user_id=admin.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso",
        message="Mensaje",
    )

    db.commit()

    response = client.post(
        f"/notifications/{notification.id_notification}/read"
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_read_notification_not_found(client):
    login_admin(client)

    response = client.post("/notifications/99999/read")

    assert response.status_code == 404


def test_read_all_notifications(client, db):
    from app.modules.notifications.notification_constants import NotificationType
    from app.modules.notifications.notification_service import create_notification
    from app.modules.users.user_model import User

    login_admin(client)

    admin = db.query(User).filter_by(nombre="Admin Principal").first()

    create_notification(
        db=db,
        user_id=admin.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso 1",
        message="Mensaje",
    )

    create_notification(
        db=db,
        user_id=admin.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso 2",
        message="Mensaje",
    )

    db.commit()

    response = client.post("/notifications/read-all")

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True
    assert data["marked"] >= 2


def test_open_notification_redirect(client, db):
    from app.modules.notifications.notification_constants import NotificationType
    from app.modules.notifications.notification_service import create_notification
    from app.modules.users.user_model import User

    login_admin(client)

    admin = db.query(User).filter_by(nombre="Admin Principal").first()

    notification = create_notification(
        db=db,
        user_id=admin.id_usuario,
        type=NotificationType.SYSTEM,
        title="Proyecto",
        message="Nuevo proyecto",
        url="/dashboard",
    )

    db.commit()

    response = client.get(
        f"/notifications/{notification.id_notification}/open",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/dashboard"


def test_open_notification_default_redirect(client, db):
    from app.modules.notifications.notification_constants import NotificationType
    from app.modules.notifications.notification_service import create_notification
    from app.modules.users.user_model import User

    login_admin(client)

    admin = db.query(User).filter_by(nombre="Admin Principal").first()

    notification = create_notification(
        db=db,
        user_id=admin.id_usuario,
        type=NotificationType.SYSTEM,
        title="Proyecto",
        message="Sin URL",
    )

    db.commit()

    response = client.get(
        f"/notifications/{notification.id_notification}/open",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/dashboard"


def test_open_notification_not_found(client):
    login_admin(client)

    response = client.get(
        "/notifications/99999/open",
        follow_redirects=False,
    )

    assert response.status_code == 404