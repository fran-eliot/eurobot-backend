# app/core/config/breadcrumbs.py

from app.modules.users.user_service import get_user_by_id

DYNAMIC_BREADCRUMBS = [
    {
        "pattern": r"^/users/(?P<id>\d+)$",
        "resolver": get_user_by_id,
        "param": "id",
        "label": lambda user: f"{user.nombre}",
    },
    {
        "pattern": r"^/users/(?P<id>\d+)/edit$",
        "resolver": get_user_by_id,
        "param": "id",
        "label": lambda user: f"Editar {user.nombre}",
    },
    # 🔥 futuro:
    # cursos, citas, etc.
]
