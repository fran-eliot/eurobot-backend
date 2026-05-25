# app/db/models.py
# Este archivo importa todos los modelos de datos utilizados en la aplicación.
# Al centralizar las importaciones de los modelos en este archivo, se facilita la
# gestión de las dependencias y se mejora la organización del código.
# Cualquier módulo que necesite acceder a los modelos puede simplemente
# importar desde este archivo, evitando importaciones circulares y manteniendo
# el código limpio y modular.

from app.modules.activities.activity_model import Activity
from app.modules.activity_attachments.activity_attachment_model import (
    ActivityAttachment,
)
from app.modules.audit.audit_model import AuditLog
from app.modules.identities.identity_model import Identity
from app.modules.notifications.notification_model import Notification
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.roles.role_model import Permission, Role
from app.modules.tasks.task_model import Task
from app.modules.users.user_model import User

# Esto le dice a Ruff que estos imports son legítimos y obligatorios
__all__ = [
    "Activity",
    "ActivityAttachment",
    "AuditLog",
    "Identity",
    "Notification",
    "ProjectMember",
    "Project",
    "Permission",
    "Role",
    "Task",
    "User",
]
