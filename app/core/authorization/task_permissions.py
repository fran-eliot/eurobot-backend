# app/core/authorization/task_permissions.py
from fastapi import HTTPException

from app.modules.projects.project_member_model import ProjectMember
from app.modules.tasks.task_model import Task

# =========================================================
# 🔍 UTILIDADES
# =========================================================


def _get_roles(user):

    return [r.nombre.lower() for r in getattr(user, "roles", [])]


def is_admin(user):

    return "admin" in _get_roles(user)


def is_student(user):

    return "estudiante" in _get_roles(user)


# =========================================================
# 👁️ VER TAREA
# =========================================================


def can_view_task(db, current_user, task: Task):

    if is_admin(current_user):
        return True

    # 👨‍🎓 estudiante → solo tareas asignadas
    if is_student(current_user):
        return task.assigned_to == current_user.id_usuario

    # 👨‍🏫 profesor/coordinator → tareas de proyectos donde participa
    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == task.project_id,
            ProjectMember.user_id == current_user.id_usuario,
        )
        .first()
    )

    return member is not None


# =========================================================
# 🛡️ REQUIRE VIEW
# =========================================================


def ensure_can_view_task(db, current_user, task):

    if not can_view_task(db, current_user, task):
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a esta tarea",
        )
