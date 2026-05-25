# scripts/seed_db/seed_audit.py
# Este archivo define la función para insertar datos de auditoría en la base de datos.

import random
from datetime import UTC, datetime

from app.modules.audit.audit_model import AuditLog


def seed_audit(db, users):
    actions = ["LOGIN", "LOGOUT", "CREATE_USER", "DELETE_USER"]

    all_users = (
        users["admins"] + users["profesores"] + users["alumnos"] + users["uah_users"]
    )

    logs = []

    for _ in range(50):
        user = random.choice(all_users)

        logs.append(
            AuditLog(
                user_id=user.id_usuario,
                action=random.choice(actions),
                resource_type="user",
                resource_id=user.id_usuario,
                description="Acción generada automáticamente",
                ip_address=f"192.168.1.{random.randint(1, 255)}",
                user_agent="Mozilla/5.0",
                created_at=datetime.now(UTC),
            )
        )

    db.add_all(logs)
    db.commit()
