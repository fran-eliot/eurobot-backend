# scripts/seed_db/seed_projects.py

from datetime import UTC, datetime, timedelta
from random import choice, randint, uniform

from app.modules.activities.activity_model import Activity
from app.modules.activity_feed.activity_feed_constants import FeedEvent
from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.tasks.task_model import Task, TaskPriorityEnum, TaskStatusEnum
from app.modules.users.user_model import User


def random_created_at(days_back: int = 30):
    return datetime.now(UTC) - timedelta(
        days=randint(0, days_back),
        hours=randint(0, 23),
        minutes=randint(0, 59),
    )


def add_feed(db, project_id, user_id, event_type, message, entity_type, entity_id):
    db.add(
        ProjectActivityFeed(
            project_id=project_id,
            user_id=user_id,
            event_type=event_type,
            message=message,
            entity_type=entity_type,
            entity_id=entity_id,
            created_at=random_created_at(30),
        )
    )


def seed_projects(db):
    print("📁 Seeding projects...")

    if db.query(Project).count() > 0:
        print("⚠️ Projects ya inicializados")
        return

    users = db.query(User).all()

    if not users:
        print("⚠️ No hay usuarios. Ejecuta seed_users primero.")
        return

    admin = db.query(User).filter_by(nombre="Admin Principal").first() or users[0]
    profesor_garcia = (
        db.query(User).filter_by(nombre="Profesor García").first() or users[0]
    )
    profesor_lopez = (
        db.query(User).filter_by(nombre="Profesor López").first() or profesor_garcia
    )
    profesor_martinez = (
        db.query(User).filter_by(nombre="Profesor Martínez").first() or profesor_garcia
    )

    alumnos = (
        db.query(User)
        .filter(User.nombre.like("Alumno %"))
        .order_by(User.id_usuario.asc())
        .all()
    )

    if len(alumnos) < 8:
        print("⚠️ Hay pocos alumnos seed. Se reutilizarán usuarios disponibles.")

    fallback_members = alumnos or users

    projects_data = [
        {
            "name": "Robot Seguidor de Línea",
            "description": (
                "Diseño y construcción de un robot autónomo capaz de seguir "
                "un circuito mediante sensores infrarrojos y control de motores."
            ),
            "status": "Activo",
            "created_by": admin.id_usuario,
            "start_date": datetime.now(UTC).date() - timedelta(days=25),
            "end_date": datetime.now(UTC).date() + timedelta(days=35),
            "coordinators": [profesor_garcia],
            "members": alumnos[0:5] if len(alumnos) >= 5 else fallback_members[:5],
        },
        {
            "name": "Brazo Robótico Inteligente",
            "description": (
                "Prototipo de brazo robótico con servomotores, cinemática básica "
                "y control manual mediante joystick."
            ),
            "status": "Activo",
            "created_by": profesor_garcia.id_usuario,
            "start_date": datetime.now(UTC).date() - timedelta(days=40),
            "end_date": datetime.now(UTC).date() + timedelta(days=50),
            "coordinators": [profesor_garcia, profesor_lopez],
            "members": alumnos[5:10] if len(alumnos) >= 10 else fallback_members[:5],
        },
        {
            "name": "Drone Educativo Modular",
            "description": (
                "Plataforma de aprendizaje STEM basada en un drone modular con "
                "telemetría, pruebas de estabilidad y documentación técnica."
            ),
            "status": "Activo",
            "created_by": profesor_lopez.id_usuario,
            "start_date": datetime.now(UTC).date() - timedelta(days=15),
            "end_date": datetime.now(UTC).date() + timedelta(days=70),
            "coordinators": [profesor_lopez],
            "members": alumnos[10:15] if len(alumnos) >= 15 else fallback_members[:5],
        },
        {
            "name": "Estación Meteorológica IoT",
            "description": (
                "Sistema IoT con sensores ambientales, recogida de datos y "
                "dashboard web para monitorización."
            ),
            "status": "Finalizado",
            "created_by": admin.id_usuario,
            "start_date": datetime.now(UTC).date() - timedelta(days=90),
            "end_date": datetime.now(UTC).date() - timedelta(days=10),
            "coordinators": [profesor_martinez],
            "members": alumnos[15:20] if len(alumnos) >= 20 else fallback_members[:5],
        },
        {
            "name": "Coche Autónomo Mini",
            "description": (
                "Vehículo autónomo educativo con sensores ultrasónicos, control "
                "PWM y detección básica de obstáculos."
            ),
            "status": "Activo",
            "created_by": profesor_martinez.id_usuario,
            "start_date": datetime.now(UTC).date() - timedelta(days=10),
            "end_date": datetime.now(UTC).date() + timedelta(days=45),
            "coordinators": [profesor_martinez, admin],
            "members": alumnos[2:8] if len(alumnos) >= 8 else fallback_members[:5],
        },
    ]

    projects = []

    for item in projects_data:
        project = Project(
            name=item["name"],
            description=item["description"],
            status=item["status"],
            start_date=item["start_date"],
            end_date=item["end_date"],
            created_by=item["created_by"],
        )

        db.add(project)
        db.flush()
        projects.append((project, item))

        add_feed(
            db,
            project.id_project,
            item["created_by"],
            FeedEvent.PROJECT_CREATED,
            f"Se creó el proyecto '<strong>{project.name}</strong>'",
            "project",
            project.id_project,
        )

    db.commit()
    print(f"✅ {len(projects)} proyectos creados")

    # =====================================================
    # MIEMBROS
    # =====================================================
    created_members = 0

    for project, item in projects:
        added_user_ids = set()

        for coordinator in item["coordinators"]:
            if coordinator.id_usuario in added_user_ids:
                continue

            db.add(
                ProjectMember(
                    project_id=project.id_project,
                    user_id=coordinator.id_usuario,
                    role="coordinator",
                )
            )
            added_user_ids.add(coordinator.id_usuario)
            created_members += 1

            add_feed(
                db,
                project.id_project,
                coordinator.id_usuario,
                FeedEvent.MEMBER_JOINED,
                f"'<strong>{coordinator.nombre}</strong>' fue añadido como coordinador",
                "user",
                coordinator.id_usuario,
            )

        for member in item["members"]:
            if member.id_usuario in added_user_ids:
                continue

            db.add(
                ProjectMember(
                    project_id=project.id_project,
                    user_id=member.id_usuario,
                    role="member",
                )
            )
            added_user_ids.add(member.id_usuario)
            created_members += 1

            add_feed(
                db,
                project.id_project,
                member.id_usuario,
                FeedEvent.MEMBER_JOINED,
                f"'<strong>{member.nombre}</strong>' fue añadido como miembro",
                "user",
                member.id_usuario,
            )

    db.commit()
    print(f"✅ {created_members} miembros de proyecto creados")

    # =====================================================
    # TAREAS
    # =====================================================
    tasks_templates = {
        "Robot Seguidor de Línea": [
            (
                "Diseñar chasis principal",
                "Diseño estructural del robot y soporte de sensores.",
                TaskStatusEnum.done,
                TaskPriorityEnum.high,
            ),
            (
                "Montar sensores IR",
                "Instalación y cableado de sensores infrarrojos.",
                TaskStatusEnum.doing,
                TaskPriorityEnum.high,
            ),
            (
                "Programar seguimiento de línea",
                "Algoritmo básico de navegación sobre circuito.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.high,
            ),
            (
                "Calibrar motores",
                "Ajuste de velocidad diferencial.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.medium,
            ),
        ],
        "Brazo Robótico Inteligente": [
            (
                "Montar estructura mecánica",
                "Montaje físico del brazo y base giratoria.",
                TaskStatusEnum.done,
                TaskPriorityEnum.medium,
            ),
            (
                "Configurar servomotores",
                "Calibración de ángulos y límites de movimiento.",
                TaskStatusEnum.doing,
                TaskPriorityEnum.high,
            ),
            (
                "Implementar control por joystick",
                "Interfaz de control manual.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.medium,
            ),
            (
                "Documentar cinemática básica",
                "Explicación técnica del movimiento.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.low,
            ),
        ],
        "Drone Educativo Modular": [
            (
                "Montar frame",
                "Ensamblado de estructura y brazos.",
                TaskStatusEnum.done,
                TaskPriorityEnum.high,
            ),
            (
                "Probar motores",
                "Validar hélices, ESC y estabilidad inicial.",
                TaskStatusEnum.doing,
                TaskPriorityEnum.high,
            ),
            (
                "Diseñar módulo de telemetría",
                "Envío de datos al panel.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.medium,
            ),
            (
                "Preparar protocolo de seguridad",
                "Normas de prueba y vuelo controlado.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.high,
            ),
        ],
        "Estación Meteorológica IoT": [
            (
                "Integrar sensores ambientales",
                "Temperatura, humedad y presión.",
                TaskStatusEnum.done,
                TaskPriorityEnum.medium,
            ),
            (
                "Crear dashboard web",
                "Visualización de datos históricos.",
                TaskStatusEnum.done,
                TaskPriorityEnum.medium,
            ),
            (
                "Preparar informe final",
                "Documentación de resultados.",
                TaskStatusEnum.done,
                TaskPriorityEnum.low,
            ),
        ],
        "Coche Autónomo Mini": [
            (
                "Montar base mecánica",
                "Ruedas, chasis y soporte de sensores.",
                TaskStatusEnum.doing,
                TaskPriorityEnum.medium,
            ),
            (
                "Implementar detección de obstáculos",
                "Sensores ultrasónicos y lógica de evasión.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.high,
            ),
            (
                "Controlar velocidad con PWM",
                "Gestión de motores DC.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.medium,
            ),
            (
                "Pruebas en circuito",
                "Validación en entorno controlado.",
                TaskStatusEnum.todo,
                TaskPriorityEnum.high,
            ),
        ],
    }

    tasks = []

    for project, item in projects:
        project_members = (
            db.query(ProjectMember)
            .filter(ProjectMember.project_id == project.id_project)
            .all()
        )

        project_users = [m.user for m in project_members if m.user] or users

        for name, description, status, priority in tasks_templates.get(
            project.name, []
        ):
            assigned_user = choice(project_users)

            task = Task(
                project_id=project.id_project,
                name=name,
                description=description,
                status=status,
                priority=priority,
                assigned_to=assigned_user.id_usuario,
                created_by=project.created_by or admin.id_usuario,
                due_date=datetime.now(UTC).date()
                + timedelta(days=choice([7, 14, 21, 30])),
            )

            db.add(task)
            db.flush()
            tasks.append(task)

            add_feed(
                db,
                project.id_project,
                task.created_by,
                FeedEvent.TASK_CREATED,
                f"Se creó la tarea '<strong>{task.name}</strong>'",
                "task",
                task.id_task,
            )

            if task.status == TaskStatusEnum.doing:
                add_feed(
                    db,
                    project.id_project,
                    assigned_user.id_usuario,
                    FeedEvent.TASK_STATUS_CHANGED,
                    f"'<strong>{task.name}</strong>' pasó a <strong>doing</strong>",
                    "task",
                    task.id_task,
                )

            if task.status == TaskStatusEnum.done:
                add_feed(
                    db,
                    project.id_project,
                    assigned_user.id_usuario,
                    FeedEvent.TASK_STATUS_CHANGED,
                    f"'<strong>{task.name}</strong>' pasó a <strong>done</strong>",
                    "task",
                    task.id_task,
                )

    db.commit()
    print(f"✅ {len(tasks)} tareas creadas")

    # =====================================================
    # ACTIVIDADES
    # =====================================================
    activity_templates = [
        "Análisis inicial",
        "Diseño técnico",
        "Montaje de componentes",
        "Cableado y conexiones",
        "Programación del módulo",
        "Pruebas funcionales",
        "Corrección de errores",
        "Optimización",
        "Documentación técnica",
        "Validación final",
    ]

    activities = []

    for task in tasks:
        project_members = (
            db.query(ProjectMember)
            .filter(ProjectMember.project_id == task.project_id)
            .all()
        )
        project_users = [m.user for m in project_members if m.user] or users

        for i in range(choice([2, 3, 4])):
            user = choice(project_users)

            activity = Activity(
                name=activity_templates[i],
                description=f"{activity_templates[i]} relacionada con la tarea {task.name}.",
                status=choice(["Pendiente", "En progreso", "Completada"]),
                task_id=task.id_task,
                user_id=user.id_usuario,
                time_spent=round(uniform(0.5, 4.5), 1),
            )

            db.add(activity)
            db.flush()
            activities.append(activity)

            add_feed(
                db,
                task.project_id,
                user.id_usuario,
                FeedEvent.ACTIVITY_CREATED,
                f"Se creó la actividad '<strong>{activity.name}</strong>'",
                "activity",
                activity.id_activity,
            )

    db.commit()
    print(f"✅ {len(activities)} actividades creadas")
    print("🚀 Seed projects PRO completado")
