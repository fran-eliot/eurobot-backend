# tests/test_activity_feed_service.py

from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed
from app.modules.activity_feed.activity_feed_service import create_feed_event
from app.modules.projects.project_model import Project
from app.modules.users.user_model import User


def get_user(db, nombre):
    return db.query(User).filter_by(nombre=nombre).first()


def create_project(db):
    project = Project(
        name="Proyecto Test",
        description="Proyecto",
        status="Activo",
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def patch_feed_events(monkeypatch):
    calls = {
        "emit_project_event": 0,
        "emit_dashboard_event": 0,
    }

    monkeypatch.setattr(
        "app.modules.activity_feed.activity_feed_service.emit_project_event",
        lambda *args, **kwargs: calls.__setitem__(
            "emit_project_event", calls["emit_project_event"] + 1
        ),
    )

    monkeypatch.setattr(
        "app.modules.activity_feed.activity_feed_service.emit_dashboard_event",
        lambda *args, **kwargs: calls.__setitem__(
            "emit_dashboard_event", calls["emit_dashboard_event"] + 1
        ),
    )

    return calls


def test_create_feed_event_with_user(monkeypatch, db):
    calls = patch_feed_events(monkeypatch)

    user = get_user(db, "Admin Principal")
    project = create_project(db)

    feed = create_feed_event(
        db=db,
        project_id=project.id_project,
        user=user,
        event_type="TASK_CREATED",
        message="Nueva tarea",
        entity_type="task",
        entity_id=1,
    )

    assert feed.id_feed is not None
    assert feed.project_id == project.id_project
    assert feed.user_id == user.id_usuario
    assert feed.event_type == "TASK_CREATED"
    assert feed.message == "Nueva tarea"
    assert feed.entity_type == "task"
    assert feed.entity_id == 1
    assert calls["emit_project_event"] == 1
    assert calls["emit_dashboard_event"] == 1


def test_create_feed_event_without_user(monkeypatch, db):
    calls = patch_feed_events(monkeypatch)

    project = create_project(db)

    feed = create_feed_event(
        db=db,
        project_id=project.id_project,
        user=None,
        event_type="SYSTEM",
        message="Evento del sistema",
    )

    assert feed.id_feed is not None
    assert feed.user_id is None
    assert feed.event_type == "SYSTEM"
    assert feed.message == "Evento del sistema"
    assert calls["emit_project_event"] == 1
    assert calls["emit_dashboard_event"] == 1


def test_create_feed_event_persists_entry(monkeypatch, db):
    patch_feed_events(monkeypatch)

    user = get_user(db, "Admin Principal")
    project = create_project(db)

    feed = create_feed_event(
        db=db,
        project_id=project.id_project,
        user=user,
        event_type="PROJECT_UPDATED",
        message="Proyecto actualizado",
        entity_type="project",
        entity_id=project.id_project,
    )

    db.commit()

    stored = (
        db.query(ProjectActivityFeed)
        .filter_by(id_feed=feed.id_feed)
        .first()
    )

    assert stored is not None
    assert stored.message == "Proyecto actualizado"