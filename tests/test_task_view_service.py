# tests/test_task_view_service.py

from datetime import UTC, datetime, timedelta

import pytest

from app.modules.audit.audit_model import AuditLog
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.tasks.task_model import Task
from app.modules.tasks.task_view_service import (
    build_task_detail_view,
    format_day_label,
)
from app.modules.users.user_model import User

# =====================================================
# HELPERS
# =====================================================


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


def add_member(db, project_id, user_id, role="member"):
    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role,
    )

    db.add(member)
    db.commit()

    return member


def create_task(db, project_id, created_by, assigned_to=None):
    task = Task(
        project_id=project_id,
        name="Task Test",
        description="Desc",
        created_by=created_by,
        assigned_to=assigned_to,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def create_audit_log(
    db,
    user_id,
    task_id,
    action="UPDATE_TASK",
    created_at=None,
):
    log = AuditLog(
        action=action,
        user_id=user_id,
        resource_type="task",
        resource_id=task_id,
        description="Cambio",
        created_at=created_at or datetime.now(UTC),
    )

    db.add(log)
    db.commit()

    return log


# =====================================================
# format_day_label
# =====================================================


def test_format_day_label_today():
    today = datetime.now(UTC).date()

    assert format_day_label(today) == "Hoy"


def test_format_day_label_yesterday():
    yesterday = datetime.now(UTC).date() - timedelta(days=1)

    assert format_day_label(yesterday) == "Ayer"


def test_format_day_label_other_date():
    old_date = datetime(2025, 1, 10, tzinfo=UTC).date()

    assert format_day_label(old_date) == "10/01/2025"


# =====================================================
# build_task_detail_view
# =====================================================


def test_build_task_detail_view_not_found(monkeypatch, db):
    admin = get_user(db, "Admin Principal")

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.can_user_action",
        lambda *args, **kwargs: True,
    )

    with pytest.raises(Exception):
        build_task_detail_view(db, 999, admin)


def test_build_task_detail_view_permission_denied(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")

    project = create_project(db)

    task = create_task(
        db,
        project.id_project,
        alumno.id_usuario,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.can_user_action",
        lambda *args, **kwargs: False,
    )

    with pytest.raises(Exception):
        build_task_detail_view(db, task.id_task, alumno)


def test_build_task_detail_view_success(monkeypatch, db):
    admin = get_user(db, "Admin Principal")
    alumno = get_user(db, "Alumno UAH")

    project = create_project(db)

    add_member(
        db,
        project.id_project,
        admin.id_usuario,
        role="coordinator",
    )

    task = create_task(
        db,
        project.id_project,
        admin.id_usuario,
        assigned_to=alumno.id_usuario,
    )

    create_audit_log(
        db,
        admin.id_usuario,
        task.id_task,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.can_user_action",
        lambda action, resource, current_user, target: True,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.get_available_users",
        lambda db, project_id: ["user1", "user2"],
    )

    result = build_task_detail_view(
        db,
        task.id_task,
        admin,
    )

    assert result["task"].id_task == task.id_task
    assert result["project"].id_project == project.id_project
    assert result["assignee"].id_usuario == alumno.id_usuario

    assert result["can_edit"] is True
    assert result["can_delete"] is True

    assert len(result["available_users"]) == 2
    assert len(result["grouped_audit"]) == 1


def test_build_task_detail_view_without_manage_permission(
    monkeypatch,
    db,
):
    admin = get_user(db, "Admin Principal")

    project = create_project(db)

    task = create_task(
        db,
        project.id_project,
        admin.id_usuario,
    )

    def fake_can_user_action(action, resource, current_user, target):
        if action == "read":
            return True

        return False

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.can_user_action",
        fake_can_user_action,
    )

    result = build_task_detail_view(
        db,
        task.id_task,
        admin,
    )

    assert result["can_edit"] is False
    assert result["can_delete"] is False
    assert result["available_users"] == []


def test_build_task_detail_view_groups_logs_by_day(
    monkeypatch,
    db,
):
    admin = get_user(db, "Admin Principal")

    project = create_project(db)

    task = create_task(
        db,
        project.id_project,
        admin.id_usuario,
    )

    today = datetime.now(UTC)

    yesterday = today - timedelta(days=1)

    create_audit_log(
        db,
        admin.id_usuario,
        task.id_task,
        created_at=today,
    )

    create_audit_log(
        db,
        admin.id_usuario,
        task.id_task,
        created_at=yesterday,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.can_user_action",
        lambda *args, **kwargs: True,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_view_service.get_available_users",
        lambda db, project_id: [],
    )

    result = build_task_detail_view(
        db,
        task.id_task,
        admin,
    )

    assert len(result["grouped_audit"]) == 2

    labels = [group["label"] for group in result["grouped_audit"]]

    assert "Hoy" in labels
    assert "Ayer" in labels