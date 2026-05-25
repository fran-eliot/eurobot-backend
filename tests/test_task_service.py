# tests/test_task_service.py
# Este archivo contiene pruebas para el módulo de servicios de tareas. Se
# verifica que las funciones relacionadas con la gestión de tareas funcionen
# correctamente. Se prueban casos como la creación de tareas, la actualización
# de su estado, y la normalización de campos. Se utilizan fixtures de pytest 
# para configurar el entorno de prueba. Se emplea monkeypatching para simular
# diferentes roles y permisos de usuario. Se verifica que se manejen 
# correctamente los casos de error, como la creación de tareas en proyectos 
# que no existen o la actualización de tareas sin los permisos adecuados.

from app.modules.projects.project_model import Project
from app.modules.tasks.task_model import Task, TaskStatusEnum
from app.modules.tasks.task_service import (
    change_task_status_with_audit,
    create_task,
    create_task_with_audit,
    delete_task_with_audit,
    normalize,
    update_task_status,
    update_task_with_audit,
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


def create_task_db(db, project_id, created_by):
    task = Task(
        project_id=project_id,
        name="Task Test",
        description="Desc",
        created_by=created_by,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# =====================================================
# normalize
# =====================================================


def test_normalize_with_none():
    assert normalize(None) == ""


def test_normalize_with_value():
    assert normalize("hola") == "hola"


# =====================================================
# create_task
# =====================================================


def test_create_task_success(monkeypatch, db):
    admin = get_user(db, "Admin Principal")

    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.tasks.task_service.can_manage_tasks",
        lambda user, project: True,
    )

    task = create_task(
        db=db,
        user=admin,
        project_id=project.id_project,
        name="Nueva tarea",
        description="Descripción",
        assigned_to=None,
    )

    assert task.id_task is not None
    assert task.name == "Nueva tarea"
    assert task.project_id == project.id_project


def test_create_task_project_not_exists(monkeypatch, db):
    admin = get_user(db, "Admin Principal")

    monkeypatch.setattr(
        "app.modules.tasks.task_service.can_manage_tasks",
        lambda user, project: True,
    )

    try:
        create_task(
            db=db,
            user=admin,
            project_id=999,
            name="Task",
            description="Desc",
            assigned_to=None,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == "Proyecto no existe"


def test_create_task_permission_denied(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")

    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.tasks.task_service.can_manage_tasks",
        lambda user, project: False,
    )

    try:
        create_task(
            db=db,
            user=alumno,
            project_id=project.id_project,
            name="Task",
            description="Desc",
            assigned_to=None,
        )

        assert False

    except PermissionError as exc:
        assert str(exc) == "No autorizado"


# =====================================================
# update_task_status
# =====================================================


def test_update_task_status_success(monkeypatch, db):
    admin = get_user(db, "Admin Principal")

    project = create_project(db)

    task = create_task_db(
        db,
        project.id_project,
        admin.id_usuario,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_service.can_manage_tasks",
        lambda user, project: True,
    )

    updated = update_task_status(
        db=db,
        user=admin,
        task_id=task.id_task,
        new_status=TaskStatusEnum.doing,
    )

    assert updated.status == TaskStatusEnum.doing


def test_update_task_status_task_not_exists(monkeypatch, db):
    admin = get_user(db, "Admin Principal")

    monkeypatch.setattr(
        "app.modules.tasks.task_service.can_manage_tasks",
        lambda user, project: True,
    )

    try:
        update_task_status(
            db=db,
            user=admin,
            task_id=999,
            new_status=TaskStatusEnum.done,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == "Task no existe"


def test_update_task_status_permission_denied(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")

    project = create_project(db)

    task = create_task_db(
        db,
        project.id_project,
        alumno.id_usuario,
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_service.can_manage_tasks",
        lambda user, project: False,
    )

    try:
        update_task_status(
            db=db,
            user=alumno,
            task_id=task.id_task,
            new_status=TaskStatusEnum.done,
        )

        assert False

    except PermissionError as exc:
        assert str(exc) == "No autorizado"


class DummyRequest:
    client = None
    headers = {}


def patch_task_side_effects(monkeypatch):
    calls = {
        "log_action": 0,
        "emit_project_event": 0,
        "create_feed_event": 0,
        "create_notification": 0,
    }

    monkeypatch.setattr(
        "app.modules.tasks.task_service.log_action",
        lambda *args, **kwargs: calls.__setitem__("log_action", calls["log_action"] + 1),
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_service.emit_project_event",
        lambda *args, **kwargs: calls.__setitem__(
            "emit_project_event", calls["emit_project_event"] + 1
        ),
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_service.create_feed_event",
        lambda *args, **kwargs: calls.__setitem__(
            "create_feed_event", calls["create_feed_event"] + 1
        ),
    )

    monkeypatch.setattr(
        "app.modules.tasks.task_service.create_notification",
        lambda *args, **kwargs: calls.__setitem__(
            "create_notification", calls["create_notification"] + 1
        ),
    )

    return calls


def test_create_task_with_audit_without_request(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)

    task = create_task_with_audit(
        db=db,
        name="Tarea sin request",
        project_id=project.id_project,
        current_user=admin,
    )

    assert task.id_task is not None
    assert task.name == "Tarea sin request"
    assert task.created_by == admin.id_usuario


def test_create_task_with_audit_with_user_and_request(monkeypatch, db):
    calls = patch_task_side_effects(monkeypatch)

    admin = get_user(db, "Admin Principal")
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    task = create_task_with_audit(
        db=db,
        name="Tarea auditada",
        project_id=project.id_project,
        current_user=admin,
        request=DummyRequest(),
        assigned_to=alumno.id_usuario,
    )

    assert task.id_task is not None
    assert calls["log_action"] == 1
    assert calls["emit_project_event"] == 1
    assert calls["create_feed_event"] == 1
    assert calls["create_notification"] == 1


def test_change_task_status_with_audit_invalid_status(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)
    task = create_task_db(db, project.id_project, admin.id_usuario)

    try:
        change_task_status_with_audit(db, task, "invalid")
        assert False
    except ValueError as exc:
        assert str(exc) == "Estado inválido"


def test_change_task_status_with_audit_same_status(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)
    task = create_task_db(db, project.id_project, admin.id_usuario)

    result = change_task_status_with_audit(db, task, "todo")

    assert result == task
    assert task.status == TaskStatusEnum.todo


def test_change_task_status_with_audit_success(monkeypatch, db):
    calls = patch_task_side_effects(monkeypatch)

    admin = get_user(db, "Admin Principal")
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    task = create_task_db(db, project.id_project, admin.id_usuario)
    task.assigned_to = alumno.id_usuario
    db.commit()

    result = change_task_status_with_audit(
        db=db,
        task=task,
        new_status="doing",
        current_user=admin,
        request=DummyRequest(),
    )

    assert result.status == TaskStatusEnum.doing
    assert calls["log_action"] == 1
    assert calls["emit_project_event"] == 1
    assert calls["create_feed_event"] == 1
    assert calls["create_notification"] == 1


def test_delete_task_with_audit(monkeypatch, db):
    calls = patch_task_side_effects(monkeypatch)

    admin = get_user(db, "Admin Principal")
    project = create_project(db)
    task = create_task_db(db, project.id_project, admin.id_usuario)

    delete_task_with_audit(
        db=db,
        task=task,
        current_user=admin,
        request=DummyRequest(),
    )

    db.commit()

    assert db.query(Task).filter_by(id_task=task.id_task).first() is None
    assert calls["log_action"] == 1
    assert calls["emit_project_event"] == 1
    assert calls["create_feed_event"] == 1


def test_update_task_with_audit_without_changes(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)
    task = create_task_db(db, project.id_project, admin.id_usuario)

    result = update_task_with_audit(
        db=db,
        task=task,
        data={
            "name": task.name,
            "description": task.description,
            "project_id": task.project_id,
            "assigned_to": task.assigned_to,
            "status": task.status,
            "priority": task.priority,
        },
    )

    assert result == task


def test_update_task_with_audit_with_changes(monkeypatch, db):
    calls = patch_task_side_effects(monkeypatch)

    admin = get_user(db, "Admin Principal")
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)
    task = create_task_db(db, project.id_project, admin.id_usuario)

    result = update_task_with_audit(
        db=db,
        task=task,
        data={
            "name": "Tarea actualizada",
            "description": "Nueva descripción",
            "project_id": project.id_project,
            "assigned_to": alumno.id_usuario,
            "status": TaskStatusEnum.doing,
            "priority": "high",
        },
        current_user=admin,
        request=DummyRequest(),
    )

    assert result.name == "Tarea actualizada"
    assert result.assigned_to == alumno.id_usuario
    assert calls["log_action"] == 1
    assert calls["emit_project_event"] == 1
    assert calls["create_feed_event"] == 1
    assert calls["create_notification"] == 1