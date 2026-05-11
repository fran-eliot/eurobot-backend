# app/modules/projects/project_members_service.py
# 📋 Servicio de miembros de proyectos: lógica de negocio relacionada con la gestión
# de los miembros dentro de los proyectos, incluyendo la asignación de roles y la
# verificación de permisos.

from sqlalchemy.orm import Session

from app.modules.projects.project_member_model import ProjectMember


def add_member(db: Session, project_id: int, user_id: int, role: str):
    existing = db.query(ProjectMember).filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()

    if existing:
        raise ValueError("Usuario ya en proyecto")

    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role
    )

    db.add(member)
    db.flush()
    db.refresh(member)

    return member


def remove_member(db: Session, project_id: int, user_id: int):
    member = db.query(ProjectMember).filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()

    if not member:
        return None

    db.delete(member)
    db.flush()

    return member