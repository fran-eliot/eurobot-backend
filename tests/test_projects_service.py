# tests/test_projects_service.py
# Este archivo contiene pruebas para el módulo de servicios de proyectos. Se
# verifica que las funciones relacionadas con la gestión de proyectos y miembros
# funcionen correctamente. Se prueban casos como la búsqueda de proyectos con
# diferentes filtros, la obtención de usuarios disponibles para un proyecto, la eliminación de miembros, y la verificación de permisos para gestionar proyectos y
# miembros. Se utilizan fixtures de pytest para configurar el entorno de 
# prueba y se emplea monkeypatching para simular diferentes roles y permisos
# de usuario.
from fastapi import HTTPException

from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.projects.projects_service import (
    ensure_can_manage_project,
    ensure_can_manage_project_members,
    ensure_can_view_project,
    get_available_users,
    remove_member,
    search_projects,
)
from app.modules.users.user_model import User


def get_user(db, nombre):
    return db.query(User).filter_by(nombre=nombre).first()


def create_project(db, name="Proyecto Test", status="Activo"):
    project = Project(name=name, description="Descripción", status=status)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def add_project_member(db, project_id, user_id, role="member"):
    member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def test_search_projects_without_user_returns_all(db):
    create_project(db, "Proyecto A")
    create_project(db, "Proyecto B")

    projects, total = search_projects(db)

    assert total == 2
    assert len(projects) == 2


def test_search_projects_admin_sees_all(db):
    admin = get_user(db, "Admin Principal")

    create_project(db, "Proyecto A")
    create_project(db, "Proyecto B")

    projects, total = search_projects(db, current_user=admin)

    assert total == 2
    assert len(projects) == 2


def test_search_projects_non_admin_only_sees_own_projects(db):
    alumno = get_user(db, "Alumno UAH")

    own_project = create_project(db, "Proyecto Propio")
    create_project(db, "Proyecto Ajeno")

    add_project_member(db, own_project.id_project, alumno.id_usuario)

    projects, total = search_projects(db, current_user=alumno)

    assert total == 1
    assert projects[0].name == "Proyecto Propio"


def test_search_projects_filters_by_search_and_status(db):
    create_project(db, "Robot Activo", status="Activo")
    create_project(db, "Robot Finalizado", status="Finalizado")
    create_project(db, "Otro Proyecto", status="Activo")

    projects, total = search_projects(
        db,
        search="Robot",
        status="Activo",
    )

    assert total == 1
    assert projects[0].name == "Robot Activo"


def test_search_projects_pagination(db):
    create_project(db, "Proyecto 1")
    create_project(db, "Proyecto 2")
    create_project(db, "Proyecto 3")

    projects, total = search_projects(db, page=1, per_page=2)

    assert total == 3
    assert len(projects) == 2


def test_get_available_users_excludes_project_members(db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    add_project_member(db, project.id_project, alumno.id_usuario)

    available_users = get_available_users(db, project.id_project)
    available_user_ids = {user.id_usuario for user in available_users}

    assert alumno.id_usuario not in available_user_ids


def test_remove_member_existing_member(db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    add_project_member(db, project.id_project, alumno.id_usuario)

    remove_member(db, project.id_project, alumno.id_usuario)

    member = (
        db.query(ProjectMember)
        .filter_by(project_id=project.id_project, user_id=alumno.id_usuario)
        .first()
    )

    assert member is None


def test_remove_member_non_existing_member_does_nothing(db):
    project = create_project(db)

    remove_member(db, project.id_project, 999)

    assert db.query(ProjectMember).count() == 0


def test_ensure_can_manage_project_members_admin(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)

    ensure_can_manage_project_members(admin, project)


def test_ensure_can_manage_project_members_coordinator(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.projects.projects_service.is_project_coordinator",
        lambda current_user, project: True,
    )

    ensure_can_manage_project_members(alumno, project)


def test_ensure_can_manage_project_members_forbidden(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.projects.projects_service.is_project_coordinator",
        lambda current_user, project: False,
    )

    try:
        ensure_can_manage_project_members(alumno, project)
        assert False
    except HTTPException as exc:
        assert exc.status_code == 403


def test_ensure_can_manage_project_admin(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)

    ensure_can_manage_project(admin, project)


def test_ensure_can_manage_project_coordinator(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.projects.projects_service.is_project_coordinator",
        lambda current_user, project: True,
    )

    ensure_can_manage_project(alumno, project)


def test_ensure_can_manage_project_forbidden(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.projects.projects_service.is_project_coordinator",
        lambda current_user, project: False,
    )

    try:
        ensure_can_manage_project(alumno, project)
        assert False
    except HTTPException as exc:
        assert exc.status_code == 403


def test_ensure_can_view_project_admin(db):
    admin = get_user(db, "Admin Principal")
    project = create_project(db)

    ensure_can_view_project(admin, project)


def test_ensure_can_view_project_member(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.projects.projects_service.user_in_project",
        lambda current_user, project: True,
    )

    ensure_can_view_project(alumno, project)


def test_ensure_can_view_project_forbidden(monkeypatch, db):
    alumno = get_user(db, "Alumno UAH")
    project = create_project(db)

    monkeypatch.setattr(
        "app.modules.projects.projects_service.user_in_project",
        lambda current_user, project: False,
    )

    try:
        ensure_can_view_project(alumno, project)
        assert False
    except HTTPException as exc:
        assert exc.status_code == 403