# app/modules/roles/roles_web.py
# 🔐 Rutas web para gestión de Roles y Permisos (RBAC)

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.core.render import render
from app.db.session import get_db
from app.modules.auth.auth_dependencies_web import require_permission_web
from app.modules.roles.role_service import (
    create_role,
    delete_role,
    get_all_permissions,
    get_all_roles,
    get_role_audit_logs,
    get_role_or_404,
    group_permissions,
    sync_role_permissions,
    update_role,
)
from app.utils.flash import flash_error, flash_success

router = APIRouter(prefix="/roles", tags=["Roles Web"])


# =========================================================
# 📋 LISTADO
# =========================================================
@router.get("/")
def roles_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ROLES, Actions.READ)),
):
    """
    Lista todos los roles.
    """

    roles = get_all_roles(db)

    return render(request, "roles/roles_list.html", {"roles": roles})


# =========================================================
# 📝 FORMULARIO (CREATE + EDIT)
# =========================================================
@router.get("/form")
@router.get("/{role_id}/edit")
def role_form(
    request: Request,
    role_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ROLES, Actions.UPDATE)),
):
    """
    Formulario unificado para crear o editar roles.
    """

    role = None

    if role_id:
        role = get_role_or_404(db, role_id)

    permissions = get_all_permissions(db)
    grouped_permissions = group_permissions(permissions)

    return render(
        request,
        "roles/roles_form.html",
        {"role": role, "grouped_permissions": grouped_permissions},
    )


# =========================================================
# 💾 GUARDAR (CREATE + UPDATE)
# =========================================================
@router.post("/form")
@router.post("/{role_id}/edit")
def role_save(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    permissions: list[int] = Form([]),
    role_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ROLES, Actions.UPDATE)),
):
    """
    Guarda rol:
    - Si existe → update
    - Si no → create
    """

    try:
        # 🔥 UPDATE
        if role_id:
            role = get_role_or_404(db, role_id)

            update_role(db, role, nombre, descripcion)
            sync_role_permissions(db, role, permissions)

            flash_success(request, "Rol actualizado correctamente")

        # 🔥 CREATE
        else:
            role = create_role(db, nombre, descripcion)
            sync_role_permissions(db, role, permissions)

            flash_success(request, "Rol creado correctamente")

        db.commit()

        return RedirectResponse("/roles/", status_code=303)

    except HTTPException as e:
        flash_error(request, e.detail)

        permissions_all = get_all_permissions(db)

        return render(
            request,
            "roles/roles_form.html",
            {"role": None, "grouped_permissions": group_permissions(permissions_all)},
        )


# =========================================================
# 🔍 DETALLE
# =========================================================
@router.get("/{role_id}")
def role_detail(
    request: Request,
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ROLES, Actions.READ)),
):
    """
    Vista detalle de rol:
    - Permisos agrupados
    - Auditoría
    """

    role = get_role_or_404(db, role_id)

    grouped_permissions = group_permissions(role.permissions)
    logs = get_role_audit_logs(db, role_id)

    return render(
        request,
        "roles/roles_detail.html",
        {"role": role, "grouped_permissions": grouped_permissions, "logs": logs},
    )


# =========================================================
# 🗑️ ELIMINAR
# =========================================================
@router.post("/{role_id}/delete")
def role_delete(
    request: Request,
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.ROLES, Actions.DELETE)),
):
    """
    Elimina un rol.
    """

    role = get_role_or_404(db, role_id)

    delete_role(db, role)

    db.commit()

    flash_success(request, "Rol eliminado correctamente")

    return RedirectResponse("/roles/", status_code=303)
