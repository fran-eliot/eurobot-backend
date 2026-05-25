# tests/test_menu_service.py
# Este archivo contiene pruebas para el servicio de menú dinámico basado en permisos.
# Se prueban casos como la generación de la estructura del menú, el filtrado por
# permisos, la marcación de elementos activos y la construcción de breadcrumbs.


from types import SimpleNamespace

from app.core.services.menu_service import (
    build_breadcrumbs,
    build_smart_breadcrumbs,
    filter_menu_by_permissions,
    get_menu_structure,
    mark_active_menu,
)


def test_get_menu_structure():
    menu = get_menu_structure()
    assert isinstance(menu, list)
    assert len(menu) > 0


def test_filter_menu_dashboard_only():
    menu = get_menu_structure()

    result = filter_menu_by_permissions(menu, lambda perm: perm == "dashboard:read")

    labels = [item["label"] for item in result]
    assert "Dashboard" in labels


def test_filter_menu_profile_without_permission():
    menu = get_menu_structure()

    result = filter_menu_by_permissions(menu, lambda perm: False)

    labels = [item["label"] for item in result]
    assert "Mi perfil" in labels


def test_mark_active_menu_simple():
    menu = get_menu_structure()
    result = mark_active_menu(menu, "/dashboard")

    dashboard = next(i for i in result if i["label"] == "Dashboard")
    assert dashboard["active"] is True


def test_mark_active_menu_child():
    menu = get_menu_structure()
    result = mark_active_menu(menu, "/users/5")

    admin = next(i for i in result if i["label"] == "Administración")
    assert admin["active"] is True
    assert admin["open"] is True


def test_build_breadcrumbs():
    menu = mark_active_menu(get_menu_structure(), "/dashboard")
    crumbs = build_breadcrumbs(menu, "/dashboard")

    assert len(crumbs) >= 1
    assert crumbs[0]["label"] == "Dashboard"


def test_build_smart_breadcrumbs_no_match():
    req = SimpleNamespace(url=SimpleNamespace(path="/unknown"))
    crumbs = build_smart_breadcrumbs([], req, None)
    assert crumbs == []
