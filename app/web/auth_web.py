# app/web/auth_web.py
# 🌐 Rutas web de autenticación

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants.audit_actions import AuditAction
from app.core.security import validate_refresh_token
from app.core.templates import templates
from app.db.session import get_db
from app.modules.audit.audit_service import log_action
from app.modules.auth.auth_service import authenticate_user, refresh_access_token

router = APIRouter()


# =========================================================
# 🔐 LOGIN PAGE
# =========================================================
@router.get("/login")
def login_page(request: Request):
    """
    Renderiza formulario de login.
    """
    return templates.TemplateResponse(request, "auth/login.html", {})


# =========================================================
# 🔐 LOGIN ACTION
# =========================================================
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Procesa login:
    - Autentica usuario
    - Genera tokens
    - Registra auditoría
    - Setea cookies
    """

    try:
        result = authenticate_user(db, email, password)

    except HTTPException:
        return templates.TemplateResponse(
            request, "auth/login.html", {"error": "Credenciales incorrectas"}
        )

    user = result["user"]

    # =========================================================
    # 🧾 AUDITORÍA
    # =========================================================
    log_action(
        db,
        action=AuditAction.LOGIN,
        user_id=user.id_usuario,
        resource_type="user",
        resource_id=user.id_usuario,
        description="Inicio de sesión",
        request=request,
    )

    db.commit()

    # =========================================================
    # 🍪 RESPONSE + COOKIES
    # =========================================================
    response = RedirectResponse(url="/dashboard", status_code=303)

    cookie_config = {
        "httponly": True,
        "samesite": "lax" if settings.DEBUG else "strict",
        "secure": not settings.DEBUG,
        "path": "/",
    }

    # 🔥 access token
    response.set_cookie(
        key="access_token", value=result["access_token"], **cookie_config
    )

    # 🔥 refresh token
    response.set_cookie(
        key="refresh_token", value=result["refresh_token"], **cookie_config
    )

    return response


# =========================================================
# 🔄 REFRESH TOKEN
# =========================================================
@router.get("/refresh")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    """
    Genera un nuevo access token a partir del refresh token.
    """

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        # 🔐 validar token
        payload = validate_refresh_token(refresh_token)

        # 🔁 generar nuevo access
        new_access_token = refresh_access_token(payload, db)

        response = RedirectResponse("/dashboard")

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="lax" if settings.DEBUG else "strict",
            secure=not settings.DEBUG,
            path="/",
        )

        return response

    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")


# =========================================================
# 🚪 LOGOUT
# =========================================================
@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    """
    Cierra sesión:
    - Intenta registrar la auditoría si hay usuario logueado
    - Elimina cookies siempre
    """

    payload = getattr(request.state, "user", None)

    if payload:
        user_id = int(payload.get("sub"))

        log_action(
            db,
            action=AuditAction.LOGOUT,
            user_id=user_id,
            resource_type="user",
            resource_id=user_id,
            description="Cierre de sesión",
            request=request,
        )
        db.commit()

    response = RedirectResponse(url="/login", status_code=303)

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return response
