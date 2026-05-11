# app/modules/dashboard/dashboard_service.py
# 📊 Servicio de métricas para el dashboard

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.activities.activity_model import Activity
from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed
from app.modules.audit.audit_model import AuditLog
from app.modules.identities.identity_model import Identity
from app.modules.projects.project_model import Project
from app.modules.roles.role_model import Role
from app.modules.tasks.task_model import Task, TaskStatusEnum
from app.modules.users.user_model import User



def get_dashboard_metrics(db: Session) -> dict:
    """
    Métricas globales del sistema para dashboard.
    """

    # =====================================================
    # 👥 USERS
    # =====================================================
    user_stats = db.query(
        func.count(User.id_usuario).label("total"),
        func.sum(User.activo.is_(True)).label("active"),
        func.sum(User.activo.is_(False)).label("inactive")
    ).one()

    # =====================================================
    # 🛡 ROLES
    # =====================================================
    total_roles = db.query(
        func.count(Role.id_rol)
    ).scalar() or 0

    # =====================================================
    # 🔐 IDENTITIES
    # =====================================================
    identities_stats = db.query(
        func.count(Identity.id).label("total"),
        func.sum(Identity.provider == "local").label("local"),
        func.sum(Identity.provider != "local").label("external")
    ).one()

    # =====================================================
    # 📁 PROJECTS
    # =====================================================
    project_stats = db.query(
        func.count(Project.id_project).label("total"),
        func.sum(Project.status == "Activo").label("active"),
        func.sum(Project.status == "Finalizado").label("finished")
    ).one()

    # =====================================================
    # ✅ TASKS
    # =====================================================
    task_stats = db.query(
        func.count(Task.id_task).label("total"),
        func.sum(Task.status == TaskStatusEnum.todo).label("pending"),
        func.sum(Task.status == TaskStatusEnum.doing).label("progress"),
        func.sum(Task.status == TaskStatusEnum.done).label("completed")
    ).one()

    completion_rate = 0

    if task_stats.total:
        completion_rate = round(
            (task_stats.completed / task_stats.total) * 100,
            1
        )

    # =====================================================
    # ⚙ ACTIVITIES
    # =====================================================
    activity_stats = db.query(
        func.count(Activity.id_activity).label("total"),
        func.coalesce(func.sum(Activity.time_spent), 0).label("hours")
    ).one()

    recent_activities = (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .limit(5)
        .all()
    )

    # =====================================================
    # 📡 PROJECT FEED
    # =====================================================

    recent_feed = (
        db.query(ProjectActivityFeed)
        .order_by(ProjectActivityFeed.created_at.desc())
        .limit(8)
        .all()
    )

    # =====================================================
    # 🧾 AUDIT LOGS
    # =====================================================
    recent_logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(10)
        .all()
    )

    # =====================================================
    # 📦 RESULT
    # =====================================================
    return {

        # USERS
        "total_users": user_stats.total or 0,
        "active_users": int(user_stats.active or 0),
        "inactive_users": int(user_stats.inactive or 0),

        # ROLES
        "total_roles": total_roles,

        # IDENTITIES
        "total_identities": identities_stats.total or 0,
        "local_identities": identities_stats.local or 0,
        "external_identities": identities_stats.external or 0,

        # PROJECTS
        "total_projects": project_stats.total or 0,
        "active_projects": int(project_stats.active or 0),
        "finished_projects": int(project_stats.finished or 0),

        # TASKS
        "total_tasks": task_stats.total or 0,
        "pending_tasks": int(task_stats.pending or 0),
        "progress_tasks": int(task_stats.progress or 0),
        "completed_tasks": int(task_stats.completed or 0),
        "completion_rate": completion_rate,

        # ACTIVITIES
        "total_activities": activity_stats.total or 0,
        "total_hours": float(activity_stats.hours or 0),

        # FEEDS
        "recent_activities": recent_activities,
        "recent_logs": recent_logs,

        # RECENT FEEDS
        "recent_feed": recent_feed,
    }