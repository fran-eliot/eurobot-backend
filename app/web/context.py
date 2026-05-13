# app/web/context.py
# 🌐 Contexto global para plantillas Jinja

from fastapi import Request

from app.core.authorization.policies import can_user_action
from app.core.authorization.project_permissions import is_project_coordinator
from app.core.authorization.roles import has_required_role
from app.core.services.menu_service import (
    build_smart_breadcrumbs,
    filter_menu_by_permissions,
    get_menu_structure,
    mark_active_menu,
)
from app.core.utils.audit_ui import get_audit_color, get_audit_icon
from app.db.session import SessionLocal
from app.modules.activity_feed.activity_feed_utils import get_feed_color, get_feed_icon
from app.modules.notifications.notification_service import count_unread_notifications, get_user_notifications
from app.utils.flash import get_flash


# =========================================================
# 🛡️ CONTEXTO FALLBACK (seguro)
# =========================================================
def get_fallback_context():
    """
    Contexto mínimo seguro cuando:
    - No hay usuario autenticado
    - O ocurre un error
    """

    return {
        "current_user_id": None,
        "current_username": None,
        "current_user_roles": [],
        "has_role": lambda *args: False,
        "has_perm": lambda *args: False,
        "is_owner": lambda target_user: False,
        "can": lambda action, resource, target=None: False,
        "is_project_coordinator": lambda *args:False,
        "menu": [],
        "breadcrumbs": [],
        "page_title": "Aula Robótica",
        "page_heading": "",
        "flash_messages": [],
        "get_audit_icon": lambda action: "fa-info-circle",
        "get_audit_color": lambda action: "bg-primary",
        "get_feed_icon": lambda event_type: "fa-info-circle",
        "get_feed_color": lambda event_type: "bg-secondary",
        "recent_notifications": [],
        "unread_notifications_count": 0,
    }


# =========================================================
# 🌐 CONTEXTO GLOBAL PRINCIPAL
# =========================================================
def get_template_context(request: Request):
    """
    Contexto global disponible en todas las plantillas.

    Incluye:
    - Usuario actual
    - Permisos
    - Helpers de autorización
    - Menú dinámico
    - Breadcrumbs
    - Flash messages
    """

    try:
        # =========================================================
        # 🔐 1. OBTENER USUARIO DESDE MIDDLEWARE
        # =========================================================
        payload = getattr(request.state, "user", None)

        if not payload:
            return get_fallback_context()

        # =========================================================
        # 👤 2. DATOS DEL USUARIO
        # =========================================================
        user_id = int(payload.get("sub") or 0)
        username = payload.get("username", "Usuario")
        roles = [r.lower() for r in payload.get("roles", [])]
        permissions = payload.get("permissions", [])

        # =========================================================
        # 🔧 3. HELPERS DE AUTORIZACIÓN
        # =========================================================

        def has_role(*allowed_roles: str) -> bool:
            return has_required_role(roles, list(allowed_roles))

        def has_perm(*required_permissions: str, mode: str = "any") -> bool:
            required = [perm.lower() for perm in required_permissions]

            if mode == "all":
                return all(p in permissions for p in required)
            else:            
                return any(p in permissions for p in required)  

        def is_owner(target_user) -> bool:
            return (
                target_user
                and getattr(target_user, "id_usuario", None) == user_id
            )

        def can(action: str, resource: str, target=None) -> bool:
            return can_user_action(action, resource, payload, target)

        # =========================================================
        # 📋 4. MENÚ DINÁMICO
        # =========================================================
        menu = filter_menu_by_permissions(
            get_menu_structure(),
            has_perm
        )

        menu = mark_active_menu(menu, request.url.path)

        # =========================================================
        # 🧭 5. BREADCRUMBS
        # =========================================================

        db = request.state.db if hasattr(request.state, "db") else None

        request.scope["db"] = db 

        if db:
            breadcrumbs = build_smart_breadcrumbs(menu, request, db)
        else:
            breadcrumbs = []

        # =========================================================
        # 🏷️ 6. TÍTULOS DINÁMICOS
        # =========================================================
        page_heading = breadcrumbs[-1]["label"] if breadcrumbs else ""
        page_title = (
            f"{page_heading} | Aula Robótica"
            if page_heading else "Aula Robótica"
        )

        # =========================================================
        # 💬 7. FLASH MESSAGES
        # =========================================================
        flash_messages = get_flash(request)

        # 8 . NOTIFICATIONS

        recent_notifications = []
        unread_notifications_count = 0

        try:
            with SessionLocal() as notification_db:
                recent_notifications = get_user_notifications(
                    notification_db,
                    user_id,
                    limit=5,
                )

                unread_notifications_count = count_unread_notifications(
                    notification_db,
                    user_id,
                )

        except Exception as e:
            print("ERROR NOTIFICATIONS CONTEXT:", e)
            recent_notifications = []
            unread_notifications_count = 0

        # =========================================================
        # 📦 8. CONTEXTO FINAL
        # =========================================================
        return {
            "current_user_id": user_id,
            "current_username": username,
            "current_user_roles": roles,

            # 🔐 helpers
            "has_role": has_role,
            "has_perm": has_perm,
            "is_owner": is_owner,
            "can": can,
            "is_project_coordinator": is_project_coordinator,

            # 🧭 navegación
            "menu": menu,
            "breadcrumbs": breadcrumbs,

            # 🏷️ UI
            "page_title": page_title,
            "page_heading": page_heading,

            # 💬 mensajes
            "flash_messages":  flash_messages,

            # 🎨 audit UI helpers
            "get_audit_icon": get_audit_icon,
            "get_audit_color": get_audit_color,

            # activity_feed helpers
            "get_feed_icon": get_feed_icon,
            "get_feed_color": get_feed_color,

            #notifications
            "recent_notifications": recent_notifications,
            "unread_notifications_count": unread_notifications_count,
        }

    except Exception as e:
        print(f"Error construyendo contexto: {e}")
        # ⚠️ Nunca romper el render de plantillas
        return get_fallback_context()