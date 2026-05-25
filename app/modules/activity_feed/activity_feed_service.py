# app/modules/activity_feed/activity_feed_service.py

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.websockets.utils import emit_dashboard_event, emit_project_event
from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed


def create_feed_event(
    db: Session,
    *,
    project_id: int,
    user=None,
    event_type: str,
    message: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
):
    feed_entry = ProjectActivityFeed(
        project_id=project_id,
        user_id=user.id_usuario if user else None,
        event_type=event_type,
        message=message,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=datetime.now(UTC),
    )

    db.add(feed_entry)
    db.flush()

    emit_project_event(
        project_id=project_id,
        payload={
            "type": "feed_event",
            "activity": {
                "feed_id": feed_entry.id_feed,
                "event_type": feed_entry.event_type,
                "message": feed_entry.message,
                "user_id": feed_entry.user_id,
                "created_at": feed_entry.created_at.isoformat(),
            },
        },
    )

    emit_dashboard_event(
        payload={
            "type": "dashboard_feed_event",
            "activity": {
                "feed_id": feed_entry.id_feed,
                "event_type": feed_entry.event_type,
                "message": feed_entry.message,
                "user_id": feed_entry.user_id,
                "created_at": feed_entry.created_at.isoformat(),
            },
        }
    )

    return feed_entry
