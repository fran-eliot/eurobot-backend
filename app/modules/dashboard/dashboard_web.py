# app/modules/dashboard/dashboard_web.py
# 🌐 Router web para dashboard

import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.core.templates import templates
from app.db.session import get_db
from app.modules.auth.auth_dependencies_web import require_permission_web
from app.modules.dashboard.dashboard_service import get_dashboard_metrics

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission_web(Resources.DASHBOARD, Actions.READ)),
):
    """
    Vista principal del dashboard.

    Requiere:
    - Permiso: dashboard:read

    Muestra:
    - Métricas de usuarios, roles, identidades, estudiantes
    - Actividad reciente (audit logs)
    """

    logger.info("Entrando al dashboard con usuario: %s", current_user.nombre)
    # Inyectamos db en el scope para acceso global en templates
    request.scope["db"] = db

    # =========================================================
    # 📊 OBTENER MÉTRICAS
    # =========================================================
    metrics = get_dashboard_metrics(db, current_user)
    print(metrics)  # Debug: imprimir métricas obtenidas

    roles = [r.nombre.lower() for r in getattr(current_user, "roles", [])]

    is_admin = "admin" in roles

    # =========================================================
    # 🎨 RENDER TEMPLATE
    # =========================================================
    try:
        return templates.TemplateResponse(
            request,
            "dashboard/dashboard.html",
            {
                **metrics,  # expandimos directamente en el contexto
                "is_admin": is_admin,
            },
        )
    except Exception as e:
        logger.exception("Error renderizando dashboard: %s", e)
        return templates.TemplateResponse(
            request,
            "dashboard/dashboard.html",
            {"error": "Error al cargar el dashboard"},
        )
