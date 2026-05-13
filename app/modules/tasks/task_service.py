# app/modules/tasks/task_service.py
# 📋 Servicio de tareas: lógica de negocio relacionada con las tareas, incluyendo
# la creación, actualización y gestión de tareas dentro de los proyectos. Este servicio
# se encarga de validar permisos, manejar la asignación de tareas a usuarios y asegurar
# que las operaciones relacionadas con las tareas se realicen de manera consistente y 
# segura.

from datetime import UTC, datetime

from sqlalchemy.orm import Session
from app.core.constants.audit_actions import AuditAction
from app.core.websockets.utils import emit_project_event
from app.modules.activity_feed.activity_feed_constants import FeedEvent
from app.modules.activity_feed.activity_feed_service import create_feed_event
from app.modules.audit.audit_service import log_action
from app.modules.tasks.task_model import Task, TaskStatusEnum
from app.modules.projects.project_model import Project
from app.core.authorization.project_permissions import can_manage_tasks
from app.modules.notifications.notification_constants import NotificationType
from app.modules.notifications.notification_service import create_notification


def create_task(
    db: Session,
    user,
    project_id: int,
    name: str,
    description: str,
    assigned_to: int | None
):
    project = db.query(Project).filter_by(id_project=project_id).first()

    if not project:
        raise ValueError("Proyecto no existe")

    if not can_manage_tasks(user, project):
        raise PermissionError("No autorizado")

    task = Task(
        project_id=project_id,
        name=name,
        description=description,
        assigned_to=assigned_to,
        created_by=user.id_usuario
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task_status(
    db: Session,
    user,
    task_id: int,
    new_status: str
):
    task = db.query(Task).filter_by(id_task=task_id).first()

    if not task:
        raise ValueError("Task no existe")

    project = task.project

    if not can_manage_tasks(user, project):
        raise PermissionError("No autorizado")

    task.status = new_status
    db.commit()

    return task


def create_task_with_audit(
    db,
    name,
    project_id,
    current_user=None,
    request=None,
    description="",
    assigned_to=None,
    status="todo",
    priority="medium"
):

    task = Task(
        name=name,
        description=description,
        project_id=project_id,
        assigned_to=assigned_to,
        status=status,
        priority=priority,
        created_by=current_user.id_usuario if current_user else None
    )

    db.add(task)
    db.flush()

    if current_user and request:
        log_action(
            db,
            action=AuditAction.CREATE_TASK,
            user_id=current_user.id_usuario,
            resource_type="task",
            resource_id=task.id_task,
            description=f"Creó tarea '{task.name}'",
            request=request
        )

        payload={
                    "type": "audit",
                    "action": AuditAction.CREATE_TASK,
                    "description": f"Creó tarea '<strong>{task.name}</strong>'",
                    "user": current_user.nombre,
                    "user_id": current_user.id_usuario,
                    "created_at": datetime.now(UTC).isoformat()
                }

        emit_project_event(
            project_id, payload)
        
        create_feed_event(
            db=db,
            project_id=task.project_id,
            user=current_user,
            event_type=FeedEvent.TASK_CREATED,
            message=f"{current_user.nombre} creó la tarea '<strong>{task.name}</strong>'",
            entity_type="task",
            entity_id=task.id_task
        )

        if task.assigned_to and current_user and task.assigned_to != current_user.id_usuario:
            create_notification(
                db=db,
                user_id=task.assigned_to,
                type=NotificationType.TASK_ASSIGNED,
                title="Nueva tarea asignada",
                message=f"Te han asignado la tarea '{task.name}'",
                entity_type="task",
                entity_id=task.id_task,
                url=f"/tasks/{task.id_task}",
            )

    return task


def change_task_status_with_audit(
    db,
    task,
    new_status,
    current_user=None,
    request=None
):
    
    try:
        new_status_enum = TaskStatusEnum(new_status)
    except ValueError:
        raise ValueError("Estado inválido")
    
    old_status = task.status

    if old_status == new_status_enum:
        return task
    
    task.status = new_status_enum

    if current_user and request:
        log_action(
            db,
            action=AuditAction.UPDATE_TASK,
            user_id=current_user.id_usuario,
            resource_type="task",
            resource_id=task.id_task,
            description=(
                f"Cambió estado: "
                f"<strong>{old_status.value}</strong> → "
                f"<strong>{new_status_enum.value}</strong>"
            ),
            request=request
        )

        # 🔥 emitir evento SIN bloquear

        payload={
                    "type": "audit",            
                    "action": AuditAction.UPDATE_TASK,
                    "description": (
                        f"Cambió estado: "
                        f"<strong>{old_status.value}</strong> → "
                        f"<strong>{new_status_enum.value}</strong>"
                    ),
                    "user": current_user.nombre,
                    "user_id": current_user.id_usuario,
                    "created_at": datetime.now(UTC).isoformat()
                }
        emit_project_event(
            project_id=task.project_id, payload=payload
        )

        # 📢 evento específico de cambio de estado para feed de actividad
        create_feed_event(
            db=db,
            project_id=task.project_id,
            user=current_user,
            event_type=FeedEvent.TASK_STATUS_CHANGED,
            message=(
                f"{current_user.nombre} movió "
                f"'<strong>{task.name}</strong>' a "
                f"<strong>{new_status_enum.value}</strong>"
            ),
            entity_type="task",
            entity_id=task.id_task
        )

        if task.assigned_to and current_user and task.assigned_to != current_user.id_usuario:
            create_notification(
                db=db,
                user_id=task.assigned_to,
                type=NotificationType.TASK_STATUS_CHANGED,
                title="Estado de tarea actualizado",
                message=f"La tarea '{task.name}' cambió a {new_status_enum.value}",
                entity_type="task",
                entity_id=task.id_task,
                url=f"/tasks/{task.id_task}",
            )

        return task
        

def delete_task_with_audit(db, task, current_user=None, request=None):

    task_id = task.id_task
    task_name = task.name
    project_id = task.project_id

    if current_user and request:
        log_action(
            db,
            action=AuditAction.DELETE_TASK,
            user_id=current_user.id_usuario,
            resource_type="task",
            resource_id=task.id_task,
            description=f"Eliminó tarea '<strong>{task.name}</strong>'",
            request=request
        )
        payload={
                    "type": "audit",
                    "action": AuditAction.DELETE_TASK,
                    "description": f"Eliminó tarea '<strong>{task.name}</strong>'",
                    "user": current_user.nombre,
                    "user_id": current_user.id_usuario,
                    "created_at": datetime.now(UTC).isoformat()
                }
        emit_project_event(
            project_id=task.project_id, payload=payload 
            )
        
        create_feed_event(
            db=db,
            project_id=project_id,
            user=current_user,
            event_type=FeedEvent.TASK_DELETED,
            message=f"{current_user.nombre} eliminó la tarea '<strong>{task_name}</strong>'",
            entity_type="task",
            entity_id=task_id,
        )

    db.delete(task)


def normalize(value):
    return value or ""


def update_task_with_audit(
    db,
    task,
    data: dict,
    current_user=None,
    request=None
):
    """
    Actualiza una task y registra auditoría de cambios.
    """

    old_assigned_to = task.assigned_to

    # 🔍 Campos auditables
    tracked_fields = {
        "name": "Nombre",
        "description": "Descripción",
        "project_id": "Proyecto",
        "assigned_to": "Asignado a",
        "status": "Estado",
        "priority": "Prioridad"
    }

    changes = []

    # =========================
    # Detectar cambios
    # =========================
    for field, label in tracked_fields.items():
        old_value = getattr(task, field)
        new_value = data.get(field)

        if normalize(old_value) != normalize(new_value):
            changes.append((label, old_value, new_value))
            setattr(task, field, new_value)

    if not changes:
        return task
    
    # =========================
    # Guardar
    # =========================
    db.flush()

    # =========================
    # Auditoría
    # =========================
    description = ", ".join(
        f"{label}: <strong>{old}</strong> → <strong>{new}</strong>"
        for label, old, new in changes
    )
    if current_user and request:
        log_action(
            db,
            action=AuditAction.UPDATE_TASK,
            user_id=current_user.id_usuario,
            resource_type="task",
            resource_id=task.id_task,
            description=description,
            request=request
        )
        payload={
                    "type": "audit",
                    "action": AuditAction.UPDATE_TASK,
                    "description": description,
                    "user": current_user.nombre,
                    "user_id": current_user.id_usuario,
                    "created_at": datetime.now(UTC).isoformat()
                }
        emit_project_event(
            project_id=task.project_id, payload=payload
        )

        create_feed_event(
            db=db,
            project_id=task.project_id,
            user=current_user,
            event_type=FeedEvent.TASK_UPDATED,
            message=f"{current_user.nombre} actualizó la tarea '<strong>{task.name}</strong>'",
            entity_type="task",
            entity_id=task.id_task,
        )

        if (
            task.assigned_to
            and old_assigned_to != task.assigned_to
            and current_user
            and task.assigned_to != current_user.id_usuario
        ):
            create_notification(
                db=db,
                user_id=task.assigned_to,
                type=NotificationType.TASK_ASSIGNED,
                title="Tarea reasignada",
                message=f"Te han asignado la tarea '{task.name}'",
                entity_type="task",
                entity_id=task.id_task,
                url=f"/tasks/{task.id_task}",
            )
        
    return task