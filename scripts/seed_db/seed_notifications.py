# scripts/seed_db/seed_notifications.py

from datetime import UTC, datetime, timedelta
from random import choice, randint

from app.modules.notifications.notification_constants import NotificationType
from app.modules.notifications.notification_model import Notification
from app.modules.tasks.task_model import Task
from app.modules.users.user_model import User


def random_date(days_back=10):
    return datetime.now(UTC) - timedelta(
        days=randint(0, days_back),
        hours=randint(0, 23),
        minutes=randint(0, 59),
    )


def seed_notifications(db):
    print("🔔 Seeding notifications...")

    if db.query(Notification).count() > 0:
        print("⚠️ Notifications ya inicializadas")
        return

    users = db.query(User).all()
    tasks = db.query(Task).all()

    if not users or not tasks:
        print("⚠️ No hay usuarios o tareas para crear notificaciones")
        return

    notifications = []

    for task in tasks[:12]:
        if not task.assigned_to:
            continue

        notifications.append(
            Notification(
                user_id=task.assigned_to,
                type=NotificationType.TASK_ASSIGNED,
                title="Tarea asignada",
                message=f"Te han asignado la tarea '{task.name}'",
                entity_type="task",
                entity_id=task.id_task,
                url=f"/tasks/{task.id_task}",
                is_read=choice([False, False, True]),
                created_at=random_date(7),
            )
        )

    for user in users[:6]:
        notifications.append(
            Notification(
                user_id=user.id_usuario,
                type=NotificationType.SYSTEM,
                title="Bienvenido/a a Aula Robótica",
                message="Ya puedes consultar tus proyectos, tareas y actividad reciente.",
                entity_type="system",
                entity_id=None,
                url="/dashboard",
                is_read=choice([False, True]),
                created_at=random_date(14),
            )
        )

    db.add_all(notifications)
    db.commit()

    print(f"✅ {len(notifications)} notificaciones creadas")