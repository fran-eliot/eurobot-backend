# app/modules/tasks/tasks_web.py

# 📋 Rutas web relacionadas con tareas: estas rutas manejan la creación, edición,
# eliminación y visualización de tareas a través de formularios HTML. Incluyen 
# validación, control de permisos utilizando las funciones definidas en 
# project_permissions.py, y también emiten eventos a través de WebSockets para 
# notificar a los usuarios en tiempo real cuando se crean o actualizan tareas, 
# mejorando la experiencia de usuario sin necesidad de refrescar la página.


from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session, joinedload

from app.core.authorization.policies import can_user_action
from app.core.websockets import manager
from app.db.session import get_db
from app.core.render import render
from app.modules.audit.audit_model import AuditLog
from app.modules.tasks.task_service import change_task_status_with_audit, create_task_with_audit, delete_task_with_audit, update_task_with_audit

from app.modules.auth.auth_dependencies_web import require_permission_web
from app.core.constants.resources import Resources
from app.core.constants.actions import Actions

from app.modules.tasks.task_model import Task, TaskStatusEnum
from app.modules.projects.project_model import Project
from app.modules.tasks.task_view_service import build_task_detail_view
from app.modules.users.user_model import User
from app.modules.projects.projects_service import get_available_users


router = APIRouter(prefix="/tasks", tags=["Tasks Web"])


# =========================================================
# 📋 LISTADO
# =========================================================
@router.get("/", response_class=HTMLResponse)
def tasks_list(
    request: Request,
    search: str = "",
    status: str = "all",
    project_id: int | None = None,
    page: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.READ)),
):
    per_page = 10

    query = db.query(Task)

    if search:
        query = query.filter(Task.name.ilike(f"%{search}%"))

    if status != "all":
        query = query.filter(Task.status == status)

    if project_id:
        query = query.filter(Task.project_id == project_id)

    total = query.count()

    tasks = (
        query.order_by(Task.id_task.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    total_pages = (total + per_page - 1) // per_page
    projects = db.query(Project).all()

    pending_count = query.filter(Task.status == "todo").count()
    progress_count = query.filter(Task.status == "doing").count()
    completed_count = query.filter(Task.status == "done").count()

    return render(
        request,
        "tasks/tasks_list.html",
        {
            "tasks": tasks,
            "projects": projects,
            "search": search,
            "status": status,
            "project_id": project_id,
            "page": page,
            "total_pages": total_pages,
            "total_count": total,
            "pending_count": pending_count,
            "progress_count": progress_count,
            "completed_count": completed_count,
        },
    )


# =========================================================
# 📝 FORM CREATE
# =========================================================
@router.get("/form")
def task_create_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.CREATE)),
):
    projects = db.query(Project).all()
    users = db.query(User).all()

    return render(
        request,
        "tasks/tasks_form.html",
        {
            "task": None,
            "projects": projects,
            "users": users,
            "available_users": users,
        },
    )


# =========================================================
# 📝 FORM EDIT
# =========================================================
@router.get("/{task_id}/edit")
def task_edit_form(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.UPDATE)),
):
    task = db.query(Task).filter(Task.id_task == task_id).first()

    if not task:
        raise HTTPException(404, "Tarea no encontrada")

    available_users = get_available_users(db, task.project_id)

    return render(
        request,
        "tasks/tasks_form.html",
        {
            "task": task,
            "projects": db.query(Project).all(),
            "users": db.query(User).all(),
            "available_users": available_users,
        },
    )


# =========================================================
# 💾 CREATE
# =========================================================
@router.post("/form")
def task_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    project_id: int = Form(...),
    assigned_to: int | None = Form(None),
    status: str = Form("todo"),
    priority: str = Form("medium"),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.CREATE)),
):
    project = db.query(Project).get(project_id)

    if not project:
        raise HTTPException(400, "Proyecto no existe")

    if not can_user_action(Actions.CREATE, Resources.TASKS, current_user, project):
        raise HTTPException(403, "No autorizado")

    task = create_task_with_audit(
        db,
        name=name,
        project_id=project_id,
        current_user=current_user,
        request=request,
        description=description,
        assigned_to=assigned_to,
        status=status,
        priority=priority
    )

    db.commit()

    return RedirectResponse(f"/tasks/{task.id_task}", status_code=303)


# =========================================================
# 💾 UPDATE
# =========================================================
@router.post("/{task_id}/edit")
def task_update(
    task_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    project_id: int = Form(...),
    assigned_to: int | None = Form(None),
    status: str = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.UPDATE)),
):
    task = db.query(Task).options(joinedload(Task.project)).get(task_id)

    if not task:
        raise HTTPException(404, "Tarea no encontrada")

    if not can_user_action(Actions.UPDATE, Resources.TASKS, current_user, task):
        raise HTTPException(403, "No autorizado")
    
    task = update_task_with_audit(
        db,
        task,
        {
            "name": name,
            "description": description,
            "project_id": project_id,
            "assigned_to": assigned_to,
            "status": status,
            "priority": priority
        },
        current_user,
        request
    )

    db.commit()

    return RedirectResponse(f"/tasks/{task.id_task}", status_code=303)


# =========================================================
# 👁️ DETALLE
# =========================================================
@router.get("/{task_id}")
def task_detail(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.READ)),
):
    context = build_task_detail_view(db, task_id,current_user)

    return render(
        request,
        "tasks/tasks_detail.html",
        context,
    )


# =========================================================
# 🗑️ DELETE
# =========================================================
@router.post("/{task_id}/delete")
def task_delete(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.DELETE)),
):
    task = db.query(Task).options(joinedload(Task.project)).get(task_id)

    if not task:
        raise HTTPException(404, "Tarea no encontrada")

    if not can_user_action(Actions.DELETE, Resources.TASKS, current_user, task):
        raise HTTPException(403, "No autorizado")
    
    delete_task_with_audit(db, task, current_user, request)
    db.commit()

    return RedirectResponse("/tasks/", status_code=303)


# =========================================================
# 🔄 CAMBIO ESTADO (KANBAN)
# =========================================================
@router.post("/{task_id}/status")
def change_task_status(
    request: Request,
    task_id: int,
    new_status: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.TASKS, Actions.UPDATE)),
):
    task = db.query(Task).options(joinedload(Task.project)).get(task_id)

    if not task:
        raise HTTPException(404, "Tarea no encontrada")

    change_task_status_with_audit(
        db,
        task,
        new_status,
        current_user,
        request
    )

    db.commit()

    return {"ok": True}