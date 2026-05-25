# app/core/services/menu_service.py
# 📋 Servicio de menú dinámico basado en permisos

import re
from functools import lru_cache

from app.core.presentation.breadcrumbs import DYNAMIC_BREADCRUMBS


# =========================================================
# 🗂️ MENÚ BASE (definición global, sin filtrar)
# =========================================================
@lru_cache
def get_menu_structure():
    """
    Definición global del menú (independiente del usuario).
    """

    return [
        {
            "label": "Dashboard",
            "icon": "fas fa-tachometer-alt",
            "url": "/dashboard",
            "permission": "dashboard:read",
        },
        {
            "label": "Administración",
            "icon": "fas fa-cogs",
            "children": [
                {
                    "label": "Usuarios",
                    "icon": "far fa-circle",
                    "url": "/users/",
                    "permission": "users:read",
                },
                {
                    "label": "Identidades",
                    "icon": "far fa-circle",
                    "url": "/identities/",
                    "permission": "identities:read",
                },
                {
                    "label": "Roles",
                    "icon": "far fa-circle",
                    "url": "/roles/",
                    "permission": "roles:read",
                },
            ],
        },
        {
            "label": "Proyectos",
            "icon": "fas fa-project-diagram",
            "children": [
                {
                    "label": "Ver proyectos",
                    "icon": "far fa-circle",
                    "url": "/projects/",
                    "permission": "projects:read",
                },
                {
                    "label": "Nuevo proyecto",
                    "icon": "far fa-circle",
                    "url": "/projects/form",
                    "permission": "projects:create",
                },
            ],
        },
        {
            "label": "Estudiantes",
            "icon": "fas fa-user-graduate",
            "url": "/students/",
            "permission": "students:read",
        },
        {"label": "Mi perfil", "icon": "fas fa-user", "url": "/users/me"},
    ]


# =========================================================
# 🔐 FILTRADO DE MENÚ POR PERMISOS
# =========================================================
def filter_menu_by_permissions(menu, has_perm):
    """
    Filtra el menú según permisos del usuario.
    """

    filtered_menu = []

    for item in menu:
        # 🔹 copiar item base
        new_item = item.copy()

        # 🔸 caso con hijos (submenu)
        if "children" in item:
            children = []

            for child in item["children"]:
                perm = child.get("permission")

                if not perm or has_perm(perm):
                    children.append(child)

            # si quedan hijos → incluir menú
            if children:
                new_item["children"] = children
                filtered_menu.append(new_item)

        else:
            perm = item.get("permission")

            if not perm or has_perm(perm):
                filtered_menu.append(new_item)

    return filtered_menu


# =========================================================
# 🧭 MARCAR MENÚ ACTIVO
# =========================================================
def mark_active_menu(menu, current_path: str):
    for item in menu:
        item["active"] = False
        item["open"] = False

        if "children" in item:
            any_child_active = False

            for child in item["children"]:
                child["active"] = current_path.startswith(child["url"])
                if child["active"]:
                    any_child_active = True

            item["active"] = any_child_active

            # abierto si tiene hijos visibles (mejor UX)
            item["open"] = len(item["children"]) > 0

        else:
            item["active"] = current_path.startswith(item.get("url", ""))

    return menu


# =========================================================
# 🧭 CONSTRUCCIÓN DE BREADCRUMBS
# =========================================================
def build_breadcrumbs(menu, current_path: str):
    breadcrumbs = []

    for item in menu:
        if item.get("active"):
            breadcrumbs.append({"label": item["label"], "url": item.get("url")})

        if "children" in item:
            for child in item["children"]:
                if child.get("active"):
                    breadcrumbs.append(
                        {"label": child["label"], "url": child.get("url")}
                    )

    return breadcrumbs


# =========================================================
# 🧭 BREADCRUMBS INTELIGENTES (con soporte para entidades dinámicas)
# =========================================================
def build_smart_breadcrumbs(menu, request, db):
    """
    Breadcrumbs inteligentes con soporte para entidades dinámicas.
    """

    path = request.url.path
    breadcrumbs = []

    # 🔹 base: menú
    for item in menu:
        if item.get("active"):
            breadcrumbs.append({"label": item["label"], "url": item.get("url")})

        if "children" in item:
            for child in item["children"]:
                if child.get("active"):
                    breadcrumbs.append(
                        {"label": child["label"], "url": child.get("url")}
                    )

    # 🔥 dinámicos declarativos
    for route in DYNAMIC_BREADCRUMBS:
        match = re.match(route["pattern"], path)

        if match:
            try:
                param_value = int(match.group(route["param"]))

                entity = route["resolver"](db, param_value)

                if not entity:
                    continue

                if "label" in route:
                    label = route["label"](entity)
                else:
                    label = getattr(entity, route["label_field", ""], "Detalle")

                breadcrumbs.append({"label": label, "url": None})

                break  # asumir solo un match

            except Exception as e:
                print("🔥 breadcrumb error:", e)

    return breadcrumbs
