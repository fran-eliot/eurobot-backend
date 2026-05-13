# app/modules/dashboard/dashboard_service.py

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.modules.activities.activity_model import Activity
from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed
from app.modules.audit.audit_model import AuditLog
from app.modules.identities.identity_model import Identity
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.roles.role_model import Role
from app.modules.tasks.task_model import Task, TaskStatusEnum
from app.modules.users.user_model import User


def get_user_role_names(current_user) -> list[str]:
    return [
        role.nombre.lower()
        for role in getattr(current_user, "roles", [])
    ]


def calculate_completion_rate(total_tasks: int, completed_tasks: int) -> float:
    if not total_tasks:
        return 0

    return round((completed_tasks / total_tasks) * 100, 1)


def empty_dashboard_metrics() -> dict:
    return {
        "total_users": 0,
        "active_users": 0,
        "inactive_users": 0,

        "total_roles": 0,

        "total_identities": 0,
        "local_identities": 0,
        "external_identities": 0,

        "total_projects": 0,
        "active_projects": 0,
        "finished_projects": 0,

        "total_tasks": 0,
        "pending_tasks": 0,
        "progress_tasks": 0,
        "completed_tasks": 0,
        "completion_rate": 0,

        "total_activities": 0,
        "total_hours": 0,

        "recent_activities": [],
        "recent_logs": [],
        "recent_feed": [],
    }


def get_dashboard_metrics(db: Session, current_user) -> dict:
    roles = get_user_role_names(current_user)

    if "admin" in roles:
        return get_admin_dashboard_metrics(db)

    return get_contextual_dashboard_metrics(db, current_user, roles)


def get_admin_dashboard_metrics(db: Session) -> dict:
    user_stats = db.query(
        func.count(User.id_usuario).label("total"),
        func.sum(User.activo.is_(True)).label("active"),
        func.sum(User.activo.is_(False)).label("inactive"),
    ).one()

    total_roles = (
        db.query(func.count(Role.id_rol))
        .scalar()
        or 0
    )

    identities_stats = db.query(
        func.count(Identity.id).label("total"),

        func.coalesce(
            func.sum(
                case(
                    (Identity.provider == "local", 1),
                    else_=0,
                )
            ),
            0,
        ).label("local"),

        func.coalesce(
            func.sum(
                case(
                    (Identity.provider != "local", 1),
                    else_=0,
                )
            ),
            0,
        ).label("external"),
    ).one()

    project_stats = db.query(
        func.count(Project.id_project).label("total"),
        func.sum(Project.status == "Activo").label("active"),
        func.sum(Project.status == "Finalizado").label("finished"),
    ).one()

    task_stats = db.query(
        func.count(Task.id_task).label("total"),
        func.sum(Task.status == TaskStatusEnum.todo).label("pending"),
        func.sum(Task.status == TaskStatusEnum.doing).label("progress"),
        func.sum(Task.status == TaskStatusEnum.done).label("completed"),
    ).one()

    activity_stats = db.query(
        func.count(Activity.id_activity).label("total"),
        func.coalesce(func.sum(Activity.time_spent), 0).label("hours"),
    ).one()

    recent_activities = (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .limit(5)
        .all()
    )

    recent_feed = (
        db.query(ProjectActivityFeed)
        .order_by(ProjectActivityFeed.created_at.desc())
        .limit(8)
        .all()
    )

    recent_logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(10)
        .all()
    )

    total_tasks = int(task_stats.total or 0)
    completed_tasks = int(task_stats.completed or 0)

    return {
        "total_users": user_stats.total or 0,
        "active_users": int(user_stats.active or 0),
        "inactive_users": int(user_stats.inactive or 0),

        "total_roles": total_roles,

        "total_identities": identities_stats.total or 0,
        "local_identities": int(identities_stats.local or 0),
        "external_identities": int(identities_stats.external or 0),

        "total_projects": project_stats.total or 0,
        "active_projects": int(project_stats.active or 0),
        "finished_projects": int(project_stats.finished or 0),

        "total_tasks": total_tasks,
        "pending_tasks": int(task_stats.pending or 0),
        "progress_tasks": int(task_stats.progress or 0),
        "completed_tasks": completed_tasks,
        "completion_rate": calculate_completion_rate(
            total_tasks,
            completed_tasks,
        ),

        "total_activities": activity_stats.total or 0,
        "total_hours": float(activity_stats.hours or 0),

        "recent_activities": recent_activities,
        "recent_logs": recent_logs,
        "recent_feed": recent_feed,
    }


def get_contextual_dashboard_metrics(
    db: Session,
    current_user,
    roles: list[str],
) -> dict:
    user_id = current_user.id_usuario

    project_ids = [
        row[0]
        for row in (
            db.query(ProjectMember.project_id)
            .filter(ProjectMember.user_id == user_id)
            .all()
        )
    ]

    if not project_ids:
        return empty_dashboard_metrics()

    projects_query = (
        db.query(Project)
        .filter(Project.id_project.in_(project_ids))
    )

    tasks_query = (
        db.query(Task)
        .filter(Task.project_id.in_(project_ids))
    )

    if "estudiante" in roles or "uah_user" in roles:
        tasks_query = tasks_query.filter(
            Task.assigned_to == user_id
        )

    total_projects = projects_query.count()

    active_projects = (
        projects_query
        .filter(Project.status == "Activo")
        .count()
    )

    finished_projects = (
        projects_query
        .filter(Project.status == "Finalizado")
        .count()
    )

    total_tasks = tasks_query.count()

    pending_tasks = (
        tasks_query
        .filter(Task.status == TaskStatusEnum.todo)
        .count()
    )

    progress_tasks = (
        tasks_query
        .filter(Task.status == TaskStatusEnum.doing)
        .count()
    )

    completed_tasks = (
        tasks_query
        .filter(Task.status == TaskStatusEnum.done)
        .count()
    )

    activity_query = (
        db.query(Activity)
        .join(Task, Activity.task_id == Task.id_task)
        .filter(Task.project_id.in_(project_ids))
    )

    if "estudiante" in roles:
        activity_query = activity_query.filter(
            Activity.user_id == current_user.id_usuario
        )

    activity_stats = (
        activity_query.with_entities(
            func.count(Activity.id_activity).label("total"),
            func.coalesce(func.sum(Activity.time_spent), 0).label("hours"),
        )
        .one()
    )

    recent_activities = (
        activity_query
        .order_by(Activity.created_at.desc())
        .limit(5)
        .all()
    )

    recent_feed = (
        db.query(ProjectActivityFeed)
        .filter(ProjectActivityFeed.project_id.in_(project_ids))
        .order_by(ProjectActivityFeed.created_at.desc())
        .limit(8)
        .all()
    )

    return {
        "total_users": 0,
        "active_users": 0,
        "inactive_users": 0,

        "total_roles": 0,

        "total_identities": 0,
        "local_identities": 0,
        "external_identities": 0,

        "total_projects": total_projects,
        "active_projects": active_projects,
        "finished_projects": finished_projects,

        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "progress_tasks": progress_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": calculate_completion_rate(
            total_tasks,
            completed_tasks,
        ),

        "total_activities": activity_stats.total or 0,
        "total_hours": float(activity_stats.hours or 0),

        "recent_activities": recent_activities,

        # No mostrar auditoría global a usuarios no admin
        "recent_logs": [],

        "recent_feed": recent_feed,
    }

