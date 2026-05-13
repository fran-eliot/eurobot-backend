# Jerarquía de roles para validación

ROLE_HIERARCHY = {
    "admin": 4,
    "profesor": 3,
    "coordinator":2,
    "estudiante": 1
}

def has_required_role(
    user_roles: list[str],
    allowed_roles: list[str]
) -> bool:
    """
    Comprueba si el usuario tiene al menos uno de los roles permitidos.
    """

    if not user_roles:
        return False

    user_roles = [r.lower() for r in user_roles]
    allowed_roles = [r.lower() for r in allowed_roles]

    return any(role in user_roles for role in allowed_roles)