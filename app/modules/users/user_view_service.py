# app/modules/users/user_view_service.py

from app.modules.roles.role_service import get_all_roles
from app.modules.users.user_service import (
    explain_user_permission,
    get_user_audit_logs,
    get_user_or_404,
    get_user_permissions,
    get_user_permissions_by_role,
    get_user_permissions_with_origin,
)


def build_user_detail_view(db, user_id):

    user = get_user_or_404(db, user_id)

    return {
        "user": user,
        "roles": get_all_roles(db),
        # 🔐 permisos
        "permissions": get_user_permissions(user),
        "permissions_by_role": get_user_permissions_by_role(user),
        "permissions_with_origin": get_user_permissions_with_origin(user),
        # 🔍 explainable RBAC
        "permission_checks": [
            {"action": "view", "result": explain_user_permission(user, "view", user)},
            {"action": "edit", "result": explain_user_permission(user, "edit", user)},
            {
                "action": "delete",
                "result": explain_user_permission(user, "delete", user),
            },
        ],
        # 📜 auditoría
        "audit_logs": get_user_audit_logs(db, user_id, limit=20),
    }
