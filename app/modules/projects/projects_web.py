# app/modules/projects/projects_web.py

# Este archivo define las rutas web para la gestión de proyectos, tareas y
# actividades. Estas rutas renderizan plantillas HTML y permiten a los usuarios
# interactuar con los proyectos a través de una interfaz web. Cada ruta incluye
# las dependencias necesarias para la autenticación, autorización y acceso a la
# base de datos, asegurando que solo los usuarios con los permisos adecuados puedan
# acceder a las funcionalidades correspondientes. Las plantillas HTML se encuentran
# en la carpeta "templates/projects" y "templates/tasks" y se utilizan para mostrar
# la información de los proyectos, tareas y actividades de manera visual y amigable.


from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


from app.core.render import render
from app.db.session import get_db

from app.modules.activity_feed.activity_feed_model import ProjectActivityFeed
from app.modules.auth.auth_dependencies_web import require_permission_web
from app.core.constants.actions import Actions
from app.core.constants.resources import Resources

from app.modules.activity_feed.activity_feed_constants import FeedEvent
from app.modules.activity_feed.activity_feed_service import create_feed_event
from app.modules.users.user_model import User

from app.modules.projects.project_members_service import add_member
from app.modules.projects.project_model import Project
from app.modules.projects.projects_service import get_available_users, remove_member, search_projects
from app.modules.tasks.task_model import Task
from app.utils.flash import flash_success

router = APIRouter(prefix="/projects", tags=["Projects Web"])


# =========================================================
# 📋 LISTADO
# =========================================================
@router.get("/")
def projects_list(
    request: Request,
    search: str = "",
    status: str = "all",
    page: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.READ,
        )
    ),
):
    per_page = 10

    projects, total = search_projects(
        db,
        search=search,
        status=status,
        page=page,
        per_page=per_page,
    )

    total_pages = (total + per_page - 1) // per_page

    return render(
        request,
        "projects/projects_list.html",
        {
            "projects": projects,
            "search": search,
            "status": status,
            "page": page,
            "total_pages": total_pages,
        },
    )

# =========================================================
# 📝 FORM CREATE
# =========================================================
@router.get("/form", name="project_form_create")
def project_create_form(
    request: Request,
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.CREATE,
        )
    ),
):
    return render(
        request,
        "projects/projects_form.html",
        {
            "project": None,
            "form_data": None,
            "errors": None,
        },
    )


# =========================================================
# 💾 CREATE
# =========================================================
@router.post("/form")
def project_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.CREATE,
        )
    ),
):
    name = name.strip()
    description = description.strip()

    errors = {}

    if not name:
        errors["name"] = "El nombre es obligatorio"

    if errors:
        return render(
            request,
            "projects/projects_form.html",
            {
                "project": None,
                "form_data": {
                    "name": name,
                    "description": description,
                },
                "errors": errors,
            },
        )

    project = Project(
        name=name,
        description=description,
        status="Activo",
        created_by=current_user.id_usuario,
    )

    db.add(project)
    db.flush()
    db.refresh(project)

    create_feed_event(
        db=db,
        project_id=project.id_project,
        user=current_user,
        event_type=FeedEvent.PROJECT_CREATED,
        message=f"{current_user.nombre} creó el proyecto '<strong>{project.name}</strong>'",
        entity_type="project",
        entity_id=project.id_project,
    )

    db.commit()

    flash_success(
        request,
        "Proyecto creado correctamente",
    )

    return RedirectResponse(
        f"/projects/{project.id_project}",
        status_code=303,
    )


# =========================================================
# 👁️ DETALLE
# =========================================================
@router.get("/{project_id}")
def project_detail(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.READ,
        )
    ),
):
    project = (
        db.query(Project)
        .filter(Project.id_project == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado",
        )

    tasks = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.id_task.desc())
        .all()
    )

    kanban = {
        "todo": [t for t in tasks if t.status.value == "todo"],
        "doing": [t for t in tasks if t.status.value == "doing"],
        "done": [t for t in tasks if t.status.value == "done"],
    }

    feed_events = (
        db.query(ProjectActivityFeed)
        .filter(
            ProjectActivityFeed.project_id == project.id_project
        )
        .order_by(ProjectActivityFeed.created_at.desc())
        .limit(20)
        .all()
    )

    members = project.members
    available_users = get_available_users(db, project.id_project)

    return render(
        request,
        "projects/projects_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "kanban": kanban,
            "feed_events": feed_events,
            "members":members,
            "avialable_users": available_users,
            "current_user":current_user,
        },
    )


# =========================================================
# 📝 FORM EDIT
# =========================================================
@router.get("/{project_id}/edit", name="project_form_edit")
def project_edit_form(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.UPDATE,
        )
    ),
):
    project = (
        db.query(Project)
        .filter(Project.id_project == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado",
        )

    return render(
        request,
        "projects/projects_form.html",
        {
            "project": project,
            "form_data": None,
            "errors": None,
        },
    )


# =========================================================
# 💾 UPDATE
# =========================================================
@router.post("/{project_id}/edit")
def project_update(
    request: Request,
    project_id: int,
    name: str = Form(...),
    description: str = Form(""),
    status: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.UPDATE,
        )
    ),
):
    project = (
        db.query(Project)
        .filter(Project.id_project == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado",
        )
    
    old_name = project.name
    old_status = project.status

    name = name.strip()
    description = description.strip()

    errors = {}

    if not name:
        errors["name"] = "El nombre es obligatorio"

    if status not in ["Activo", "Finalizado"]:
        errors["status"] = "Estado inválido"

    if errors:
        return render(
            request,
            "projects/projects_form.html",
            {
                "project": project,
                "form_data": {
                    "name": name,
                    "description": description,
                    "status": status,
                },
                "errors": errors,
            },
        )

    project.name = name
    project.description = description
    project.status = status

    db.flush()

    if old_name != name or old_status != status:
        create_feed_event(
            db=db,
            project_id=project.id_project,
            user=current_user,
            event_type=FeedEvent.PROJECT_UPDATED,
            message=f"{current_user.nombre} actualizó el proyecto '<strong>{project.name}</strong>'",
            entity_type="project",
            entity_id=project.id_project,
        )

    db.commit()

    flash_success(
        request,
        "Proyecto actualizado correctamente",
    )

    return RedirectResponse(
        f"/projects/{project.id_project}",
        status_code=303,
    )


# =========================================================
# 🗑️ DELETE
# =========================================================
@router.post("/{project_id}/delete")
def project_delete(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.DELETE,
        )
    ),
):
    project = (
        db.query(Project)
        .filter(Project.id_project == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado",
        )

    db.delete(project)
    db.commit()

    flash_success(
        request,
        "Proyecto eliminado correctamente",
    )

    return RedirectResponse(
        "/projects/",
        status_code=303,
    )

# =========================================================
# ➕ ADD MEMBER
# =========================================================
@router.post("/{project_id}/members")
def add_project_member(
    request: Request,
    project_id: int,
    user_id: int = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.UPDATE,
        )
    ),
):
    
    project = db.query(Project).filter(
        Project.id_project == project_id
    ).first()

    if not project:
        raise HTTPException(404, "Proyecto no encontrado")

    user = db.query(User).filter(
        User.id_usuario == user_id
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    
    add_member(db, project_id, user_id, role)

    create_feed_event(
        db=db,
        project_id=project_id,
        user=current_user,
        event_type=FeedEvent.MEMBER_JOINED,
        message=(
            f"{current_user.nombre} añadió a "
            f"'<strong>{user.nombre}</strong>' como "
            f"<strong>{role}</strong>"
        ),
        entity_type="user",
        entity_id=user_id,
    )

    db.commit()

    flash_success(request, "Miembro añadido correctamente")

    return RedirectResponse(
        f"/projects/{project_id}",
        status_code=303,
    )


# =========================================================
# 🗑️ DELETE MEMBER
# =========================================================
@router.post("/{project_id}/members/{user_id}/delete")
def delete_member(
    request: Request,
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.PROJECTS,
            Actions.UPDATE
        )
    ),
):
    project = db.query(Project).filter(
        Project.id_project == project_id
    ).first()

    if not project:
        raise HTTPException(404, "Proyecto no encontrado")

    user = db.query(User).filter(
        User.id_usuario == user_id
    ).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    member = remove_member(db, project_id, user_id)

    if member:
        create_feed_event(
            db=db,
            project_id=project_id,
            user=current_user,
            event_type=FeedEvent.MEMBER_REMOVED,
            message=(
                f"{current_user.nombre} eliminó a "
                f"'<strong>{user.nombre}</strong>' del proyecto"
            ),
            entity_type="user",
            entity_id=user_id,
        )

    db.commit()

    return RedirectResponse(
        f"/projects/{project_id}",
        status_code=303
    )

