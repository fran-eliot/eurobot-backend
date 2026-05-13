# app/core/authorization/activity_permissions.py

from fastapi import HTTPException

from app.modules.activities.activity_model import Activity
from app.modules.projects.project_member_model import ProjectMember


def _roles(user):
    return [
        r.nombre.lower()
        for r in getattr(user, "roles", [])
    ]


def is_admin(user):
    return "admin" in _roles(user)


def is_student(user):
    return "estudiante" in _roles(user)


def can_view_activity(db, current_user, activity: Activity):
    if is_admin(current_user):
        return True

    if is_student(current_user):
        return (
            activity.user_id == current_user.id_usuario
        )

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == activity.task.project_id,
            ProjectMember.user_id == current_user.id_usuario,
        )
        .first()
    )

    return member is not None


def ensure_can_view_activity(db, current_user, activity):
    if not can_view_activity(db, current_user, activity):
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a esta actividad",
        )