# app/modules/identities/identities_web.py

from math import ceil

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload

from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.core.render import render
from app.core.security import hash_password
from app.core.templates import templates
from app.db.session import get_db
from app.modules.auth.auth_dependencies_web import require_permission_web
from app.modules.identities.identity_model import Identity
from app.modules.roles.role_model import Role
from app.modules.users.user_model import User
from app.utils.flash import flash_error, flash_success

router = APIRouter(prefix="/identities", tags=["Identities Web"])


# =========================================================
# 📋 LISTADO
# =========================================================
@router.get("/")
def identities_list(request: Request, db: Session = Depends(get_db)):
    # ================= QUERY PARAMS =================
    search = request.query_params.get("search", "").strip()
    provider = request.query_params.get("provider", "all")
    page = int(request.query_params.get("page", 1))
    per_page = 10

    # ================= BASE QUERY =================
    query = db.query(Identity).options(joinedload(Identity.usuario))

    # ================= SEARCH =================
    if search:
        query = query.filter(Identity.email.ilike(f"%{search}%"))

    # ================= FILTER PROVIDER =================
    if provider != "all":
        query = query.filter(Identity.provider == provider)

    # ================= PAGINATION =================
    total = query.count()
    total_pages = ceil(total / per_page) if total else 1

    identities = query.offset((page - 1) * per_page).limit(per_page).all()

    # ================= RENDER =================
    return render(
        request,
        "identities/identities_list.html",
        {
            "identities": identities,
            "search": search,
            "provider": provider,
            "page": page,
            "total_pages": total_pages,
        },
    )


# =========================================================
# 📝 FORM (CREATE + EDIT)
# =========================================================
@router.get("/form")
@router.get("/{identity_id}/edit")
def identity_form(
    request: Request,
    identity_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.IDENTITIES, Actions.UPDATE)),
):
    identity = None

    if identity_id:
        identity = db.get(Identity, identity_id)

    users = db.query(User).all()
    roles = db.query(Role).all()

    return templates.TemplateResponse(
        request,
        "identities/identity_form.html",
        {"identity": identity, "users": users, "roles": roles, "errors": None},
    )


# =========================================================
# 💾 SAVE (CREATE + UPDATE)
# =========================================================
@router.post("/form")
@router.post("/{identity_id}/edit")
def identity_save(
    request: Request,
    email: str = Form(...),
    password: str = Form(None),
    user_id: int = Form(...),
    identity_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.IDENTITIES, Actions.UPDATE)),
):

    identity = None

    if identity_id:
        identity = db.get(Identity, identity_id)

    # =========================================================
    # CREATE
    # =========================================================
    if not identity:
        existing = db.query(Identity).filter(Identity.email == email).first()

        if existing:
            flash_error(request, "Email ya registrado")
            return RedirectResponse("/identities/form", status_code=303)

        identity = Identity(
            email=email,
            password_hash=hash_password(password),
            user_id=user_id,
            provider="local",
        )

        db.add(identity)
        flash_success(request, "Identidad creada correctamente")

    # =========================================================
    # UPDATE
    # =========================================================
    else:
        identity.email = email
        identity.user_id = user_id

        if password:
            identity.password_hash = hash_password(password)

        flash_success(request, "Identidad actualizada")

    db.commit()

    return RedirectResponse("/identities/", status_code=303)


@router.get("/{identity_id}")
def identity_detail(
    request: Request,
    identity_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.IDENTITIES, Actions.READ)),
):
    identity = db.get(Identity, identity_id)

    if not identity:
        raise HTTPException(status_code=404, detail="Identidad no encontrada")

    return templates.TemplateResponse(
        request, "identities/identity_detail.html", {"identity": identity}
    )


# =========================================================
# ❌ DELETE
# =========================================================
@router.post("/{identity_id}/delete")
def identity_delete(
    identity_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.IDENTITIES, Actions.DELETE)),
):
    identity = db.get(Identity, identity_id)

    if identity:
        db.delete(identity)
        db.commit()

    return RedirectResponse("/identities/", status_code=303)
