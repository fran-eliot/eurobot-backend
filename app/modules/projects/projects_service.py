# app/modules/projects/projects_service.py
# 📋 Servicio de proyectos: lógica de negocio relacionada con proyectos, tareas y
# actividades.


from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.authorization.project_permissions import (
    is_project_coordinator,
    user_in_project,
)
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.users.user_model import User


def search_projects(
    db: Session,
    search: str = "",
    status: str = "all",
    page: int = 1,
    per_page: int = 10,
    current_user=None,
):
    query = db.query(Project)

    if current_user:
        roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

        if "admin" not in roles:
            query = query.join(ProjectMember).filter(
                ProjectMember.user_id == current_user.id_usuario
            )

    if search:
        query = query.filter(Project.name.ilike(f"%{search}%"))

    if status != "all":
        query = query.filter(Project.status == status)

    total = query.count()

    projects = (
        query.order_by(Project.id_project.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return projects, total


def get_available_users(db, project_id):
    subquery = db.query(ProjectMember.user_id).filter_by(project_id=project_id)
    return db.query(User).filter(~User.id_usuario.in_(subquery)).all()


def remove_member(db, project_id, user_id):
    member = (
        db.query(ProjectMember)
        .filter_by(project_id=project_id, user_id=user_id)
        .first()
    )

    if member:
        db.delete(member)
        db.commit()


def ensure_can_manage_project_members(current_user, project):
    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    if "admin" in roles:
        return

    if is_project_coordinator(current_user, project):
        return

    raise HTTPException(
        status_code=403,
        detail="No tienes permisos para gestionar miembros de este proyecto",
    )


def ensure_can_manage_project(current_user, project):
    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    if "admin" in roles:
        return

    if is_project_coordinator(current_user, project):
        return

    raise HTTPException(
        status_code=403,
        detail="No tienes permisos para gestionar este proyecto",
    )


def ensure_can_view_project(current_user, project):
    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    if "admin" in roles:
        return

    if user_in_project(current_user, project):
        return

    raise HTTPException(
        status_code=403,
        detail="No tienes acceso a este proyecto",
    )
