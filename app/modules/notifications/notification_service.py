# app/modules/notifications/notification_service.py

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.websockets.utils import emit_user_event
from app.modules.notifications.notification_model import Notification


def create_notification(
    db: Session,
    *,
    user_id: int,
    type: str,
    title: str,
    message: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
    url: str | None = None,
):
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        entity_type=entity_type,
        entity_id=entity_id,
        url=url,
        is_read=False,
        created_at=datetime.now(UTC),
    )

    db.add(notification)
    db.flush()

    emit_user_event(
        user_id=user_id,
        payload={
            "type": "notification",
            "notification": {
                "id_notification": notification.id_notification,
                "notification_type": notification.type,
                "title": notification.title,
                "message": notification.message,
                "url": notification.url,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat(),
            },
        },
    )

    return notification


def get_user_notifications(
    db: Session,
    user_id: int,
    limit: int = 10,
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .all()
    )


def count_unread_notifications(
    db: Session,
    user_id: int,
):
    return (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
        .count()
    )


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    user_id: int,
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id_notification == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )

    if not notification:
        return None

    notification.is_read = True
    notification.read_at = datetime.now(UTC)

    db.flush()

    return notification


def mark_all_notifications_as_read(
    db: Session,
    user_id: int,
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True
        notification.read_at = datetime.now(UTC)

    db.flush()

    return len(notifications)