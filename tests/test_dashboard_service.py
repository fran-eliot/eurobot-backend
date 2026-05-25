# tests/test_dashboard_service.py

from datetime import UTC, datetime

from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed
from app.modules.audit.audit_model import AuditLog
from app.modules.dashboard.dashboard_service import (
    calculate_completion_rate,
    empty_dashboard_metrics,
    get_admin_dashboard_metrics,
    get_contextual_dashboard_metrics,
    get_dashboard_metrics,
    get_user_role_names,
)
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.tasks.task_model import Task, TaskStatusEnum
from app.modules.users.user_model import User


# =====================================================
# HELPERS
# =====================================================


def get_user(db, nombre):
    return db.query(User).filter_by(nombre=nombre).first()


def create_project(db, status="Activo"):
    project = Project(
        name=f"Proyecto {status}",
        description="Proyecto",
        status=status,
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


def create_task(
    db,
    project_id,
    created_by,
    status=TaskStatusEnum.todo,
    assigned_to=None,
):
    task = Task(
        project_id=project_id,
        name="Task",
        description="Desc",
        created_by=created_by,
        assigned_to=assigned_to,
        status=status,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def create_feed(db, project_id, user_id):
    feed = ProjectActivityFeed(
        project_id=project_id,
        user_id=user_id,
        event_type="TASK_CREATED",
        message="Nueva tarea",
        created_at=datetime.now(UTC),
    )

    db.add(feed)
    db.commit()

    return feed


def create_audit(db, user_id):
    log = AuditLog(
        action="LOGIN",
        user_id=user_id,
        resource_type="auth",
        description="Login",
        created_at=datetime.now(UTC),
    )

    db.add(log)
    db.commit()

    return log


# =====================================================
# BASIC HELPERS
# =====================================================


def test_get_user_role_names(db):
    admin = get_user(db, "Admin Principal")

    roles = get_user_role_names(admin)

    assert isinstance(roles, list)
    assert "admin" in roles


def test_calculate_completion_rate_zero():
    assert calculate_completion_rate(0, 0) == 0


def test_calculate_completion_rate_normal():
    assert calculate_completion_rate(10, 7) == 70.0


def test_empty_dashboard_metrics():
    metrics = empty_dashboard_metrics()

    assert metrics["total_users"] == 0
    assert metrics["total_projects"] == 0
    assert metrics["recent_feed"] == []


# =====================================================
# ADMIN DASHBOARD
# =====================================================


def test_get_admin_dashboard_metrics(db):
    admin = get_user(db, "Admin Principal")
    alumno = get_user(db, "Alumno UAH")

    active_project = create_project(db, "Activo")
    finished_project = create_project(db, "Finalizado")

    create_task(
        db,
        active_project.id_project,
        admin.id_usuario,
        status=TaskStatusEnum.todo,
    )

    create_task(
        db,
        active_project.id_project,
        admin.id_usuario,
        status=TaskStatusEnum.doing,
    )

    create_task(
        db,
        finished_project.id_project,
        admin.id_usuario,
        status=TaskStatusEnum.done,
    )

    create_feed(
        db,
        active_project.id_project,
        admin.id_usuario,
    )

    create_audit(
        db,
        alumno.id_usuario,
    )

    metrics = get_admin_dashboard_metrics(db)

    assert metrics["total_projects"] >= 2
    assert metrics["active_projects"] >= 1
    assert metrics["finished_projects"] >= 1

    assert metrics["total_tasks"] >= 3
    assert metrics["pending_tasks"] >= 1
    assert metrics["progress_tasks"] >= 1
    assert metrics["completed_tasks"] >= 1

    assert metrics["completion_rate"] > 0

    assert isinstance(metrics["recent_feed"], list)
    assert isinstance(metrics["recent_logs"], list)
    assert isinstance(metrics["recent_activities"], list)


# =====================================================
# CONTEXTUAL DASHBOARD
# =====================================================


def test_get_contextual_dashboard_without_projects(db):
    alumno = get_user(db, "Alumno UAH")

    metrics = get_contextual_dashboard_metrics(
        db,
        alumno,
        ["estudiante"],
    )

    assert metrics["total_projects"] == 0
    assert metrics["total_tasks"] == 0


def test_get_contextual_dashboard_with_projects(db):
    admin = get_user(db, "Admin Principal")
    alumno = get_user(db, "Alumno UAH")

    project = create_project(db)

    add_member(
        db,
        project.id_project,
        alumno.id_usuario,
        role="member",
    )

    create_task(
        db,
        project.id_project,
        admin.id_usuario,
        status=TaskStatusEnum.todo,
        assigned_to=alumno.id_usuario,
    )

    create_task(
        db,
        project.id_project,
        admin.id_usuario,
        status=TaskStatusEnum.done,
        assigned_to=alumno.id_usuario,
    )

    create_feed(
        db,
        project.id_project,
        admin.id_usuario,
    )

    metrics = get_contextual_dashboard_metrics(
        db,
        alumno,
        ["estudiante"],
    )

    assert metrics["total_projects"] >= 1
    assert metrics["total_tasks"] >= 2
    assert metrics["completed_tasks"] >= 1
    assert metrics["completion_rate"] > 0

    assert isinstance(metrics["recent_feed"], list)


# =====================================================
# GENERIC DASHBOARD
# =====================================================


def test_get_dashboard_metrics_admin(db):
    admin = get_user(db, "Admin Principal")

    metrics = get_dashboard_metrics(db, admin)

    assert "total_users" in metrics
    assert "total_projects" in metrics


def test_get_dashboard_metrics_contextual(db):
    alumno = get_user(db, "Alumno UAH")

    metrics = get_dashboard_metrics(db, alumno)

    assert isinstance(metrics, dict)