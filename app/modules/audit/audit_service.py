# app/modules/audit/audit_service.py

from datetime import UTC, datetime

from fastapi import Request
from sqlalchemy.orm import Session

from app.modules.audit.audit_model import AuditLog


def log_action(
    db: Session,
    action: str,
    user_id: int | None = None,
    resource_type: str | None = None,
    resource_id: int | None = None,
    description: str | None = None,
    request: Request | None = None,
):

    log = AuditLog(
        action=action,
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None,
        created_at=datetime.now(UTC),
    )

    db.add(log)
    db.flush()


def audit_user_action(db, action, current_user, target_user, request, description):
    log_action(
        db,
        action=action,
        user_id=current_user.id_usuario,
        resource_type="user",
        resource_id=target_user.id_usuario,
        description=description,
        request=request,
    )
