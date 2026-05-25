# app/core/authorization/policies.py
# Politicas de autorización personalizadas


def can_user_action(action, resource, user_payload, target=None):
    """
    Sistema unificado:
    - RBAC global
    - Permisos por proyecto
    - Compatible JWT y ORM
    """

    roles = []
    permissions = []
    user_id = None

    # =========================
    # Extraer usuario
    # =========================
    if isinstance(user_payload, dict):
        roles = [str(r).lower() for r in user_payload.get("roles", [])]
        permissions = user_payload.get("permissions", [])
        user_id = int(user_payload.get("sub"))

    else:
        user_id = getattr(user_payload, "id_usuario", None)

        raw_roles = getattr(user_payload, "roles_token", None) or getattr(
            user_payload, "roles", []
        )

        roles = [
            r.lower() if isinstance(r, str) else r.nombre.lower() for r in raw_roles
        ]

        permissions = getattr(user_payload, "permissions", [])

    # =========================
    # ADMIN bypass
    # =========================
    if "admin" in roles:
        return True

    # =========================
    # PERMISOS GLOBALES
    # =========================
    permission_name = f"{resource}:{action}"

    if permission_name in permissions:
        return True

    # =========================
    # CONTEXTO PROYECTO
    # =========================
    project = None

    if target:
        if hasattr(target, "members"):  # Project
            project = target
        elif hasattr(target, "project"):  # Task
            project = target.project

    if resource == "tasks" and project:
        members = getattr(project, "members", [])

        is_member = any(m.user_id == user_id for m in members)

        is_coordinator = any(
            m.user_id == user_id and m.role == "coordinator" for m in members
        )

        if action == "read":
            return is_member

        if action in ["create", "update", "delete"]:
            return is_coordinator

    # =========================
    # OWNER fallback
    # =========================
    target_id = getattr(target, "id_usuario", None)

    if action in ["read", "update"] and user_id == target_id:
        return True

    return False
