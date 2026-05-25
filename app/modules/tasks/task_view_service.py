# app/modules/tasks/task_view_service.py

# =========================================================
# 📝 TASK DETAIL VIEW SERVICE
# ---------------------------------------------------------
# Este servicio se encarga de construir la vista detallada de una tarea, incluyendo
# la información de la tarea, su proyecto asociado, el usuario asignado y los logs de
# auditoría relacionados. Utiliza SQLAlchemy para realizar consultas eficientes y
# cargar las relaciones necesarias para mostrar toda la información relevante en la
# vista de detalles de la tarea. Este servicio se puede utilizar tanto en la interfaz
# web como en la API para proporcionar una vista completa de la tarea a los usuarios
# autorizados.

from collections import defaultdict
from datetime import UTC, datetime, timedelta
from http.client import HTTPException

from sqlalchemy.orm import joinedload

from app.core.authorization.policies import can_user_action
from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.modules.audit.audit_model import AuditLog
from app.modules.projects.projects_service import get_available_users
from app.modules.tasks.task_model import Task


def format_day_label(date):
    today = datetime.now(UTC).date()
    yesterday = today - timedelta(days=1)

    if date == today:
        return "Hoy"
    elif date == yesterday:
        return "Ayer"
    else:
        return date.strftime("%d/%m/%Y")


def build_task_detail_view(db, task_id, current_user):

    task = (
        db.query(Task)
        .options(joinedload(Task.project), joinedload(Task.assignee))
        .filter(Task.id_task == task_id)
        .first()
    )

    if not task:
        raise HTTPException(404, "Tarea no encontrada")

    if not can_user_action(Actions.READ, Resources.TASKS, current_user, task):
        raise HTTPException(403, "No autorizado")

    can_manage = can_user_action(Actions.UPDATE, Resources.TASKS, current_user, task)

    available_users = get_available_users(db, task.project_id) if can_manage else []

    # 📜 auditoría
    audit_logs = (
        db.query(AuditLog)
        .options(joinedload(AuditLog.user))
        .filter(AuditLog.resource_type == "task", AuditLog.resource_id == task_id)
        .order_by(AuditLog.created_at.desc())
        .limit(20)
        .all()
    )

    grouped_audit = defaultdict(list)

    for log in audit_logs:
        day = log.created_at.date()
        grouped_audit[day].append(log)

    # ordenar por fecha real
    grouped_audit = dict(sorted(grouped_audit.items(), reverse=True))

    # construir estructura final
    final_grouped = []

    for day, logs in grouped_audit.items():
        final_grouped.append({"label": format_day_label(day), "logs": logs})

    return {
        "task": task,
        "grouped_audit": final_grouped,
        "available_users": available_users,
        "project": task.project,
        "assignee": task.assignee,
        # 🔐 permisos preparados para UI
        "can_edit": can_manage,
        "can_delete": can_user_action(
            Actions.DELETE, Resources.TASKS, current_user, task
        ),
    }
