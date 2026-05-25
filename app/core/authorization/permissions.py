# app/core/authorization/permissions.py

from app.core.authorization.role_permissions import ROLE_PERMISSIONS


def has_permission(
    user_permissions: list[str], required_permissions: list[str]
) -> bool:
    """
    Comprueba si el usuario tiene al menos uno de los permisos requeridos.
    """

    if not user_permissions:
        return False

    user_permissions_normalized = [p.lower() for p in user_permissions]
    required_permissions_normalized = [p.lower() for p in required_permissions]

    return any(
        perm in user_permissions_normalized for perm in required_permissions_normalized
    )


def has_permission_from_roles(
    user_roles: list[str], required_permissions: list[str]
) -> bool:

    if not user_roles:
        return False

    user_roles = [r.lower() for r in user_roles]
    required_permissions = set(p.lower() for p in required_permissions)

    for role in user_roles:
        permissions = ROLE_PERMISSIONS.get(role, [])

        # Admin total
        if "*" in permissions:
            return True

        if required_permissions.intersection(permissions):
            return True

    return False


def get_permissions_from_roles(user_roles: list[str]) -> list[str]:
    """
    Devuelve todos los permisos agregados a partir de los roles del usuario.
    """

    if not user_roles:
        return []

    user_roles = [r.lower() for r in user_roles]

    permissions = []

    for role in user_roles:
        role_permissions = ROLE_PERMISSIONS.get(role, [])

        # Admin total
        if "*" in role_permissions:
            return ["*"]

        permissions.extend(role_permissions)

    return list(set(permissions))


def can_access_resource(current_user, owner_id, permissions):
    if current_user.id_usuario == owner_id:
        return True

    return has_permission(current_user.permissions, permissions)
