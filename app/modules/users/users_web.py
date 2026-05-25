# app/modules/users/users_web.py

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.core.render import render
from app.core.templates import templates

# 🧰 Utils
from app.core.utils.validation import format_pydantic_errors
from app.db.session import get_db

# 🔐 Auth / permisos
from app.modules.auth.auth_dependencies_web import (
    get_current_user_web,
    require_owner_or_permission_web,
    require_permission_and_not_self_web,
    require_permission_web,
)
from app.modules.roles.role_service import get_all_roles

# 📦 Schemas
from app.modules.users.user_schemas import UserUpdate

# 🧠 Services
from app.modules.users.user_service import (
    create_user_with_audit,
    delete_user_with_audit,
    get_user_by_id,
    get_user_or_404,
    search_users,
    set_user_active_with_audit,
    sync_user_roles,
    update_user_with_audit,
)
from app.modules.users.user_view_service import build_user_detail_view
from app.utils.flash import flash_success
from app.web.context import get_template_context

router = APIRouter(prefix="/users", tags=["Users Web"])


# =========================================================
# 📋 LISTADO
# =========================================================
@router.get("/")
def users_list(
    request: Request,
    search: str = "",
    status: str = "all",
    page: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.USERS, Actions.READ)),
):
    per_page = 10

    users, total = search_users(
        db,
        search=search,
        status=status,
        page=page,
        per_page=per_page,
    )

    total_pages = (total + per_page - 1) // per_page

    return render(
        request,
        "users/users_list.html",
        {
            "users": users,
            "search": search,
            "status": status,
            "page": page,
            "total_pages": total_pages,
        },
    )


# =========================================================
# 📝 FORM CREATE
# =========================================================
@router.get("/form", name="user_form_create")
def user_create_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.USERS, Actions.CREATE)),
):
    return templates.TemplateResponse(
        request,
        "users/users_form.html",
        {
            **get_template_context(request),
            "user": None,
            "roles": get_all_roles(db),
            "form_data": None,
            "errors": None,
        },
    )


# =========================================================
# 📝 FORM EDIT
# =========================================================
@router.get("/{user_id}/edit", name="user_form_edit")
def user_edit_form(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    target_user=Depends(
        require_owner_or_permission_web(Resources.USERS, Actions.UPDATE)
    ),
):
    return templates.TemplateResponse(
        request,
        "users/users_form.html",
        {
            **get_template_context(request),
            "user": target_user,
            "roles": get_all_roles(db),
            "form_data": None,
            "errors": None,
        },
    )


# =========================================================
# 💾 CREATE
# =========================================================
@router.post("/form")
def user_create(
    request: Request,
    nombre: str = Form(...),
    activo: bool = Form(False),
    roles: list[int] | None = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.USERS, Actions.CREATE)),
):
    roles = roles or []

    try:
        data = UserUpdate(nombre=nombre, activo=activo)

    except ValidationError as e:
        return templates.TemplateResponse(
            request,
            "users/users_form.html",
            {
                **get_template_context(request),
                "user": None,
                "roles": get_all_roles(db),
                "form_data": {
                    "nombre": nombre,
                    "activo": activo,
                    "roles": roles,
                },
                "errors": format_pydantic_errors(e.errors()),
            },
        )

    user = create_user_with_audit(
        db,
        data.nombre,
        current_user,
        request,
    )

    user.activo = data.activo if data.activo is not None else True

    sync_user_roles(db, user, roles)

    db.commit()

    flash_success(request, "Usuario creado correctamente")

    return RedirectResponse(
        f"/users/{user.id_usuario}",
        status_code=303,
    )


# =========================================================
# 💾 UPDATE
# =========================================================
@router.post("/{user_id}/edit")
def user_update(
    request: Request,
    user_id: int,
    nombre: str = Form(...),
    activo: bool = Form(False),
    roles: list[int] | None = Form(None),
    db: Session = Depends(get_db),
    target_user=Depends(
        require_owner_or_permission_web(Resources.USERS, Actions.UPDATE)
    ),
    current_user=Depends(get_current_user_web),
):
    roles = roles or []

    try:
        data = UserUpdate(nombre=nombre, activo=activo)

    except ValidationError as e:
        return templates.TemplateResponse(
            request,
            "users/users_form.html",
            {
                **get_template_context(request),
                "user": target_user,
                "roles": get_all_roles(db),
                "form_data": {
                    "nombre": nombre,
                    "activo": activo,
                    "roles": roles,
                },
                "errors": format_pydantic_errors(e.errors()),
            },
        )

    update_user_with_audit(
        db,
        target_user,
        data.nombre,
        current_user,
        request,
    )

    target_user.activo = data.activo if data.activo is not None else target_user.activo

    sync_user_roles(db, target_user, roles)

    db.commit()

    flash_success(request, "Usuario actualizado correctamente")

    return RedirectResponse(
        f"/users/{target_user.id_usuario}",
        status_code=303,
    )


# =========================================================
# 👤 DETALLE
# =========================================================
@router.get("/{user_id}")
def user_detail(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    target_user=Depends(require_owner_or_permission_web(Resources.USERS, Actions.READ)),
):
    context = build_user_detail_view(
        db,
        target_user.id_usuario,
    )

    return render(
        request,
        "users/user_detail.html",
        context,
    )


# =========================================================
# 🙋 MI PERFIL
# =========================================================
@router.get("/me", name="my_profile")
def my_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_web),
):
    context = build_user_detail_view(
        db,
        current_user.id_usuario,
    )

    return render(
        request,
        "users/user_detail.html",
        context,
    )


# =========================================================
# 🔐 ROLES
# =========================================================
@router.post("/{user_id}/roles")
def update_user_roles_view(
    request: Request,
    user_id: int,
    roles: list[int] | None = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.USERS, Actions.UPDATE)),
):
    roles = roles or []

    user = get_user_by_id(db, user_id)

    sync_user_roles(db, user, roles)

    db.commit()

    flash_success(request, "Roles actualizados correctamente")

    return RedirectResponse(
        f"/users/{user_id}",
        status_code=303,
    )


# =========================================================
# 🗑️ DELETE
# =========================================================
@router.post("/{user_id}/delete")
def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_and_not_self_web(Resources.USERS, Actions.DELETE)
    ),
):
    user = get_user_or_404(db, user_id)

    delete_user_with_audit(
        db,
        user,
        current_user,
        request,
    )

    db.commit()

    flash_success(request, "Usuario eliminado correctamente")

    return RedirectResponse(
        "/users/",
        status_code=303,
    )


# =========================================================
# 🔄 DEACTIVATE
# =========================================================
@router.post("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    target_user=Depends(
        require_owner_or_permission_web(Resources.USERS, Actions.UPDATE)
    ),
    current_user=Depends(get_current_user_web),
):
    set_user_active_with_audit(
        db,
        target_user,
        False,
        current_user,
        request,
    )

    db.commit()

    flash_success(request, "Usuario desactivado")

    return RedirectResponse(
        f"/users/{target_user.id_usuario}",
        status_code=303,
    )


# =========================================================
# 🔄 ACTIVATE
# =========================================================
@router.post("/{user_id}/activate")
def activate_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    target_user=Depends(
        require_owner_or_permission_web(Resources.USERS, Actions.UPDATE)
    ),
    current_user=Depends(get_current_user_web),
):
    set_user_active_with_audit(
        db,
        target_user,
        True,
        current_user,
        request,
    )

    db.commit()

    flash_success(request, "Usuario activado")

    return RedirectResponse(
        f"/users/{target_user.id_usuario}",
        status_code=303,
    )
