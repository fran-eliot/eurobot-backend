# tests/test_project_members_service.py

import pytest

from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_members_service import add_member, remove_member
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


def test_add_member_success(db):
    user = get_user(db, "Alumno UAH")
    project = create_project(db)

    member = add_member(
        db=db,
        project_id=project.id_project,
        user_id=user.id_usuario,
        role="member",
    )

    assert member.id is not None
    assert member.project_id == project.id_project
    assert member.user_id == user.id_usuario
    assert str(member.role) in {"member", "ProjectRoleEnum.member"}


def test_add_member_duplicate_raises_value_error(db):
    user = get_user(db, "Alumno UAH")
    project = create_project(db)

    add_member(
        db=db,
        project_id=project.id_project,
        user_id=user.id_usuario,
        role="member",
    )

    with pytest.raises(ValueError) as exc:
        add_member(
            db=db,
            project_id=project.id_project,
            user_id=user.id_usuario,
            role="member",
        )

    assert str(exc.value) == "Usuario ya en proyecto"


def test_remove_member_existing_returns_true(db):
    user = get_user(db, "Alumno UAH")
    project = create_project(db)

    add_member(
        db=db,
        project_id=project.id_project,
        user_id=user.id_usuario,
        role="member",
    )

    result = remove_member(
        db=db,
        project_id=project.id_project,
        user_id=user.id_usuario,
    )

    db.flush()

    assert result is True

    member = (
        db.query(ProjectMember)
        .filter_by(project_id=project.id_project, user_id=user.id_usuario)
        .first()
    )

    assert member is None


def test_remove_member_missing_returns_false(db):
    project = create_project(db)

    result = remove_member(
        db=db,
        project_id=project.id_project,
        user_id=999,
    )

    assert result is False