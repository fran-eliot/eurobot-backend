from types import SimpleNamespace

from app.core.services.menu_service import (
    build_breadcrumbs,
    build_smart_breadcrumbs,
    filter_menu_by_permissions,
    get_menu_structure,
    mark_active_menu,
)

# =========================================================
# 🔐 FILTER MENU - CASOS NO CUBIERTOS
# =========================================================


def test_filter_menu_children_partial_permissions():
    """
    Solo algunos hijos pasan el filtro.
    Debe mantener el padre con hijos filtrados.
    """
    menu = get_menu_structure()

    result = filter_menu_by_permissions(
        menu,
        lambda perm: perm in ["users:read"],  # solo uno
    )

    admin = next(i for i in result if i["label"] == "Administración")

    assert "children" in admin
    assert len(admin["children"]) == 1
    assert admin["children"][0]["label"] == "Usuarios"


def test_filter_menu_no_children_visible():
    """
    Si ningún hijo tiene permiso, el padre NO debe aparecer.
    """
    menu = get_menu_structure()

    result = filter_menu_by_permissions(
        menu,
        lambda perm: False,  # nadie pasa
    )

    labels = [item["label"] for item in result]

    assert "Administración" not in labels


def test_filter_menu_item_without_permission():
    """
    Items sin permission siempre deben aparecer.
    """
    menu = get_menu_structure()

    result = filter_menu_by_permissions(menu, lambda perm: False)

    labels = [item["label"] for item in result]

    assert "Mi perfil" in labels


# =========================================================
# 🧭 MARK ACTIVE MENU - EDGE CASES
# =========================================================


def test_mark_active_menu_no_match():
    """
    Ningún item debería estar activo.
    """
    menu = get_menu_structure()
    result = mark_active_menu(menu, "/no-existe")

    assert all(not item["active"] for item in result)


def test_mark_active_menu_child_exact_match():
    """
    Activación exacta de un child.
    """
    menu = get_menu_structure()
    result = mark_active_menu(menu, "/users/")

    admin = next(i for i in result if i["label"] == "Administración")

    assert admin["active"] is True
    assert admin["open"] is True

    users = next(c for c in admin["children"] if c["label"] == "Usuarios")
    assert users["active"] is True


# =========================================================
# 🧭 BREADCRUMBS - CASOS EXTRA
# =========================================================


def test_build_breadcrumbs_with_child():
    """
    Breadcrumb debe incluir padre + hijo activo.
    """
    menu = mark_active_menu(get_menu_structure(), "/users/1")
    crumbs = build_breadcrumbs(menu, "/users/1")

    labels = [c["label"] for c in crumbs]

    assert "Administración" in labels
    assert "Usuarios" in labels


def test_build_breadcrumbs_empty():
    """
    Si no hay activos, breadcrumbs vacío.
    """
    menu = mark_active_menu(get_menu_structure(), "/no-match")
    crumbs = build_breadcrumbs(menu, "/no-match")

    assert crumbs == []


# =========================================================
# 🧭 SMART BREADCRUMBS - RAMAS COMPLEJAS
# =========================================================


def test_build_smart_breadcrumbs_with_dynamic_match(monkeypatch):
    """
    Simula un breadcrumb dinámico válido.
    """

    # Mock de entidad
    class FakeEntity:
        nombre = "Entidad Test"

    def fake_resolver(db, id):
        return FakeEntity()

    # Mock de DYNAMIC_BREADCRUMBS
    monkeypatch.setattr(
        "app.core.services.menu_service.DYNAMIC_BREADCRUMBS",
        [
            {
                "pattern": r"^/roles/(?P<id>\d+)$",
                "param": "id",
                "resolver": fake_resolver,
                "label": lambda e: e.nombre,
            }
        ],
    )

    request = SimpleNamespace(url=SimpleNamespace(path="/roles/1"))

    crumbs = build_smart_breadcrumbs([], request, None)

    assert len(crumbs) == 1
    assert crumbs[0]["label"] == "Entidad Test"


def test_build_smart_breadcrumbs_entity_not_found(monkeypatch):
    """
    Si el resolver devuelve None, no añade breadcrumb.
    """

    def fake_resolver(db, id):
        return None

    monkeypatch.setattr(
        "app.core.services.menu_service.DYNAMIC_BREADCRUMBS",
        [
            {
                "pattern": r"^/roles/(?P<id>\d+)$",
                "param": "id",
                "resolver": fake_resolver,
                "label": lambda e: "Nunca",
            }
        ],
    )

    request = SimpleNamespace(url=SimpleNamespace(path="/roles/1"))

    crumbs = build_smart_breadcrumbs([], request, None)

    assert crumbs == []


def test_build_smart_breadcrumbs_exception(monkeypatch):
    """
    Si el resolver lanza excepción → no rompe.
    """

    def fake_resolver(db, id):
        raise Exception("boom")

    monkeypatch.setattr(
        "app.core.services.menu_service.DYNAMIC_BREADCRUMBS",
        [
            {
                "pattern": r"^/roles/(?P<id>\d+)$",
                "param": "id",
                "resolver": fake_resolver,
                "label": lambda e: "Error",
            }
        ],
    )

    request = SimpleNamespace(url=SimpleNamespace(path="/roles/1"))

    crumbs = build_smart_breadcrumbs([], request, None)

    assert crumbs == []
