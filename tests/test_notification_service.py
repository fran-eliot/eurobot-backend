# tests/test_notification_service.py

from app.modules.notifications.notification_constants import NotificationType
from app.modules.notifications.notification_model import Notification
from app.modules.notifications.notification_service import (
    count_unread_notifications,
    create_notification,
    get_user_notifications,
    mark_all_notifications_as_read,
    mark_notification_as_read,
)
from app.modules.users.user_model import User


def get_user(db, nombre):
    return db.query(User).filter_by(nombre=nombre).first()


def test_create_notification(monkeypatch, db):
    calls = {"emit_user_event": 0}

    monkeypatch.setattr(
        "app.modules.notifications.notification_service.emit_user_event",
        lambda *args, **kwargs: calls.__setitem__(
            "emit_user_event", calls["emit_user_event"] + 1
        ),
    )

    user = get_user(db, "Alumno UAH")

    notification = create_notification(
        db=db,
        user_id=user.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso",
        message="Mensaje de prueba",
        entity_type="project",
        entity_id=1,
        url="/projects/1",
    )

    assert notification.id_notification is not None
    assert notification.user_id == user.id_usuario
    assert notification.type == NotificationType.SYSTEM
    assert notification.title == "Aviso"
    assert notification.message == "Mensaje de prueba"
    assert notification.entity_type == "project"
    assert notification.entity_id == 1
    assert notification.url == "/projects/1"
    assert notification.is_read is False
    assert calls["emit_user_event"] == 1


def test_get_user_notifications_returns_limited_results(monkeypatch, db):
    monkeypatch.setattr(
        "app.modules.notifications.notification_service.emit_user_event",
        lambda *args, **kwargs: None,
    )

    user = get_user(db, "Alumno UAH")

    for index in range(3):
        create_notification(
            db=db,
            user_id=user.id_usuario,
            type=NotificationType.SYSTEM,
            title=f"Aviso {index}",
            message="Mensaje",
        )

    db.commit()

    notifications = get_user_notifications(db, user.id_usuario, limit=2)

    assert len(notifications) == 2


def test_count_unread_notifications(monkeypatch, db):
    monkeypatch.setattr(
        "app.modules.notifications.notification_service.emit_user_event",
        lambda *args, **kwargs: None,
    )

    user = get_user(db, "Alumno UAH")

    create_notification(
        db=db,
        user_id=user.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso 1",
        message="Mensaje",
    )
    read_notification = create_notification(
        db=db,
        user_id=user.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso 2",
        message="Mensaje",
    )

    read_notification.is_read = True
    db.commit()

    assert count_unread_notifications(db, user.id_usuario) == 1


def test_mark_notification_as_read(monkeypatch, db):
    monkeypatch.setattr(
        "app.modules.notifications.notification_service.emit_user_event",
        lambda *args, **kwargs: None,
    )

    user = get_user(db, "Alumno UAH")

    notification = create_notification(
        db=db,
        user_id=user.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso",
        message="Mensaje",
    )

    db.commit()

    result = mark_notification_as_read(
        db=db,
        notification_id=notification.id_notification,
        user_id=user.id_usuario,
    )

    assert result is not None
    assert result.is_read is True
    assert result.read_at is not None


def test_mark_notification_as_read_not_found(db):
    user = get_user(db, "Alumno UAH")

    result = mark_notification_as_read(
        db=db,
        notification_id=999,
        user_id=user.id_usuario,
    )

    assert result is None


def test_mark_all_notifications_as_read(monkeypatch, db):
    monkeypatch.setattr(
        "app.modules.notifications.notification_service.emit_user_event",
        lambda *args, **kwargs: None,
    )

    user = get_user(db, "Alumno UAH")

    create_notification(
        db=db,
        user_id=user.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso 1",
        message="Mensaje",
    )
    create_notification(
        db=db,
        user_id=user.id_usuario,
        type=NotificationType.SYSTEM,
        title="Aviso 2",
        message="Mensaje",
    )

    db.commit()

    marked = mark_all_notifications_as_read(db, user.id_usuario)

    assert marked == 2
    assert count_unread_notifications(db, user.id_usuario) == 0


def test_mark_all_notifications_as_read_without_unread(db):
    user = get_user(db, "Alumno UAH")

    marked = mark_all_notifications_as_read(db, user.id_usuario)

    assert marked == 0