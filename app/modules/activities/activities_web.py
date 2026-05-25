# app/modules/activities/activities_web.py
# 🌐 Router web para actividades


from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload

from app.core.authorization.activity_permissions import ensure_can_view_activity
from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.core.render import render
from app.db.session import get_db
from app.modules.activities.activity_model import Activity
from app.modules.activity_attachments.activity_attachment_model import (
    ActivityAttachment,
)
from app.modules.activity_feed.activity_feed_constants import FeedEvent
from app.modules.activity_feed.activity_feed_service import create_feed_event
from app.modules.auth.auth_dependencies_web import require_permission_web
from app.modules.projects.project_member_model import ProjectMember
from app.modules.tasks.task_model import Task
from app.modules.users.user_model import User
from app.utils.flash import flash_success

router = APIRouter(prefix="/activities", tags=["Activities Web"])


# =====================================================
# LISTADO
# =====================================================
@router.get("/")
def activities_list(
    request: Request,
    search: str = "",
    status: str = "all",
    task_id: int | None = None,
    page: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.READ)),
):
    per_page = 10

    query = db.query(Activity)

    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    query = query.join(Activity.task)

    if "admin" not in roles:
        if "estudiante" in roles:
            query = query.filter(Activity.user_id == current_user.id_usuario)
        else:
            project_ids = [
                row[0]
                for row in db.query(ProjectMember.project_id)
                .filter(ProjectMember.user_id == current_user.id_usuario)
                .all()
            ]

            query = query.filter(Task.project_id.in_(project_ids))

    if search:
        query = query.filter(Activity.name.ilike(f"%{search}%"))

    if status != "all":
        query = query.filter(Activity.status == status)

    if task_id:
        query = query.filter(Activity.task_id == task_id)

    stats_query = query

    total = query.count()

    activities = (
        query.order_by(Activity.id_activity.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    total_pages = (total + per_page - 1) // per_page

    if "admin" in roles:
        tasks = db.query(Task).all()
    else:
        project_ids = [
            row[0]
            for row in db.query(ProjectMember.project_id)
            .filter(ProjectMember.user_id == current_user.id_usuario)
            .all()
        ]

        tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()

    pending_count = stats_query.filter(Activity.status == "Pendiente").count()

    progress_count = stats_query.filter(Activity.status == "En progreso").count()

    completed_count = stats_query.filter(Activity.status == "Completada").count()

    return render(
        request,
        "activities/activities_list.html",
        {
            "activities": activities,
            "tasks": tasks,
            "search": search,
            "status": status,
            "task_id": task_id,
            "page": page,
            "total_pages": total_pages,
            "total_count": total,
            "pending_count": pending_count,
            "progress_count": progress_count,
            "completed_count": completed_count,
        },
    )


# =====================================================
# FORM CREATE
# =====================================================
@router.get("/form")
def activity_create_form(
    request: Request,
    task_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.CREATE)),
):
    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    if "admin" in roles:
        tasks = db.query(Task).all()
    else:
        project_ids = [
            row[0]
            for row in db.query(ProjectMember.project_id)
            .filter(ProjectMember.user_id == current_user.id_usuario)
            .all()
        ]

        tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()

    users = [current_user] if "estudiante" in roles else db.query(User).all()

    return render(
        request,
        "activities/activities_form.html",
        {
            "activity": None,
            "tasks": tasks,
            "users": users,
            "task_id": task_id,
            "errors": None,
            "form_data": None,
        },
    )


# =====================================================
# CREATE
# =====================================================
@router.post("/form")
def activity_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    status: str = Form("Pendiente"),
    task_id: int = Form(...),
    user_id: int | None = Form(None),
    time_spent: float = Form(0),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.CREATE)),
):
    task = db.query(Task).filter(Task.id_task == task_id).first()

    if not task:
        raise HTTPException(404, "Tarea no encontrada")

    fake_activity = Activity(
        name=name,
        task=task,
        task_id=task.id_task,
        user_id=user_id or current_user.id_usuario,
    )

    ensure_can_view_activity(db, current_user, fake_activity)

    if "estudiante" in [r.nombre.lower() for r in getattr(current_user, "roles", [])]:
        user_id = current_user.id_usuario

    activity = Activity(
        name=name,
        description=description,
        status=status,
        task_id=task_id,
        user_id=user_id,
        time_spent=time_spent,
    )

    db.add(activity)
    db.flush()
    db.refresh(activity)

    create_feed_event(
        db=db,
        project_id=task.project_id,
        user=current_user,
        event_type=FeedEvent.ACTIVITY_CREATED,
        message=(
            f"{current_user.nombre} creó la actividad "
            f"'<strong>{activity.name}</strong>'"
        ),
        entity_type="activity",
        entity_id=activity.id_activity,
    )

    db.commit()

    flash_success(request, "Actividad creada correctamente")

    return RedirectResponse(
        f"/activities/{activity.id_activity}",
        status_code=303,
    )


# =====================================================
# DETAIL
# =====================================================
@router.get("/{activity_id}")
def activity_detail(
    activity_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.READ)),
):
    activity = (
        db.query(Activity)
        .options(
            joinedload(Activity.task).joinedload(Task.project),
            joinedload(Activity.user),
            joinedload(Activity.attachments).joinedload(ActivityAttachment.uploader),
        )
        .filter(Activity.id_activity == activity_id)
        .first()
    )

    if not activity:
        raise HTTPException(404, "Actividad no encontrada")

    ensure_can_view_activity(db, current_user, activity)

    return render(
        request,
        "activities/activities_detail.html",
        {"activity": activity},
    )


# =====================================================
# FORM EDIT
# =====================================================
@router.get("/{activity_id}/edit")
def activity_edit_form(
    activity_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.UPDATE)),
):
    activity = (
        db.query(Activity)
        .options(
            joinedload(Activity.task).joinedload(Task.project),
            joinedload(Activity.user),
        )
        .filter(Activity.id_activity == activity_id)
        .first()
    )

    if not activity:
        raise HTTPException(404, "Actividad no encontrada")

    ensure_can_view_activity(db, current_user, activity)

    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    if "admin" in roles:
        tasks = db.query(Task).all()
    else:
        project_ids = [
            row[0]
            for row in db.query(ProjectMember.project_id)
            .filter(ProjectMember.user_id == current_user.id_usuario)
            .all()
        ]

        tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()

    users = [current_user] if "estudiante" in roles else db.query(User).all()

    return render(
        request,
        "activities/activities_form.html",
        {
            "activity": activity,
            "tasks": tasks,
            "users": users,
            "task_id": activity.task_id,
            "errors": None,
            "form_data": None,
        },
    )


# =====================================================
# UPDATE
# =====================================================
@router.post("/{activity_id}/edit")
def activity_update(
    activity_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    status: str = Form(...),
    task_id: int = Form(...),
    user_id: int | None = Form(None),
    time_spent: float = Form(0),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.UPDATE)),
):
    activity = (
        db.query(Activity)
        .options(
            joinedload(Activity.task).joinedload(Task.project),
            joinedload(Activity.user),
        )
        .filter(Activity.id_activity == activity_id)
        .first()
    )

    if not activity:
        raise HTTPException(404, "Actividad no encontrada")

    ensure_can_view_activity(db, current_user, activity)

    old_name = activity.name
    old_status = activity.status

    new_task = db.query(Task).filter(Task.id_task == task_id).first()

    if not new_task:
        raise HTTPException(404, "Tarea no encontrada")

    fake_activity = Activity(
        task=new_task,
        task_id=new_task.id_task,
        user_id=user_id or current_user.id_usuario,
    )

    ensure_can_view_activity(
        db,
        current_user,
        fake_activity,
    )

    activity.name = name
    activity.description = description
    activity.status = status
    activity.task_id = task_id
    activity.user_id = user_id
    activity.time_spent = time_spent

    db.flush()

    if old_name != name or old_status != status:
        create_feed_event(
            db=db,
            project_id=activity.task.project_id,
            user=current_user,
            event_type=FeedEvent.ACTIVITY_UPDATED,
            message=(
                f"{current_user.nombre} actualizó la actividad '"
                f"<strong>{activity.name}</strong>'",
            ),
            entity_type="activity",
            entity_id=activity.id_activity,
        )

    db.commit()

    flash_success(request, "Actividad actualizada correctamente")

    return RedirectResponse(
        f"/activities/{activity.id_activity}",
        status_code=303,
    )


# =====================================================
# DELETE
# =====================================================
@router.post("/{activity_id}/delete")
def activity_delete(
    activity_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ACTIVITIES, Actions.DELETE)),
):
    activity = (
        db.query(Activity)
        .options(
            joinedload(Activity.task).joinedload(Task.project),
            joinedload(Activity.user),
        )
        .filter(Activity.id_activity == activity_id)
        .first()
    )

    if not activity:
        raise HTTPException(404, "Actividad no encontrada")

    ensure_can_view_activity(db, current_user, activity)

    activity_name = activity.name
    project_id = activity.task.project_id
    activity_id = activity.id_activity

    create_feed_event(
        db=db,
        project_id=project_id,
        user=current_user,
        event_type=FeedEvent.ACTIVITY_DELETED,
        message=(
            f"{current_user.nombre} eliminó la actividad "
            f"'<strong>{activity_name}</strong>'"
        ),
        entity_type="activity",
        entity_id=activity_id,
    )

    db.delete(activity)
    db.commit()

    flash_success(request, "Actividad eliminada correctamente")

    return RedirectResponse(
        "/activities/",
        status_code=303,
    )
