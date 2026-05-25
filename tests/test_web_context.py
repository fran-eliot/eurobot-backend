# tests/test_web_context.py
# Este archivo contiene pruebas para el contexto global de las plantillas Jinja en
# la aplicación. Se verifica que el contexto se construya correctamente tanto en
# situaciones normales como en casos de error o ausencia de usuario. Se utilizan
# técnicas de monkeypatching para simular diferentes escenarios y validar que el
# contexto se comporte como se espera, incluyendo la generación de breadcrumbs y
# la gestión de mensajes flash.

from types import SimpleNamespace

from app.web.context import (
    get_fallback_context,
    get_template_context,
)

# =====================================================
# Helpers
# =====================================================


class DummyRequest:
    def __init__(self):
        self.state = SimpleNamespace()
        self.url = SimpleNamespace(path="/dashboard")
        self.scope = {}


# =====================================================
# fallback directo
# =====================================================


def test_get_fallback_context():
    ctx = get_fallback_context()

    assert ctx["current_user_id"] is None
    assert ctx["menu"] == []
    assert ctx["breadcrumbs"] == []
    assert ctx["page_title"] == "Aula Robótica"


# =====================================================
# sin usuario -> fallback
# =====================================================


def test_template_context_without_user():
    request = DummyRequest()

    ctx = get_template_context(request)

    assert ctx["current_user_id"] is None
    assert ctx["page_title"] == "Aula Robótica"


# =====================================================
# con usuario y sin db
# =====================================================


def test_template_context_user_without_db(monkeypatch):
    request = DummyRequest()

    request.state.user = {
        "sub": "1",
        "username": "Fran",
        "roles": ["Admin"],
        "permissions": ["users:read", "users:update"],
    }

    monkeypatch.setattr(
        "app.web.context.get_menu_structure", lambda: [{"label": "Users"}]
    )

    monkeypatch.setattr(
        "app.web.context.filter_menu_by_permissions", lambda menu, has_perm: menu
    )

    monkeypatch.setattr("app.web.context.mark_active_menu", lambda menu, path: menu)

    monkeypatch.setattr("app.web.context.get_flash", lambda request: ["ok"])

    ctx = get_template_context(request)

    assert ctx["current_user_id"] == 1
    assert ctx["current_username"] == "Fran"
    assert ctx["current_user_roles"] == ["admin"]
    assert ctx["breadcrumbs"] == []
    assert ctx["flash_messages"] == ["ok"]

    assert ctx["has_role"]("admin") is True
    assert ctx["has_perm"]("users:read") is True
    assert ctx["has_perm"]("users:read", "fake", mode="all") is False


# =====================================================
# con db y breadcrumbs
# =====================================================


def test_template_context_with_db(monkeypatch):
    request = DummyRequest()

    request.state.user = {
        "sub": "2",
        "username": "Laura",
        "roles": ["Teacher"],
        "permissions": ["dashboard:read"],
    }

    request.state.db = object()

    monkeypatch.setattr("app.web.context.get_menu_structure", lambda: [])

    monkeypatch.setattr(
        "app.web.context.filter_menu_by_permissions", lambda menu, has_perm: menu
    )

    monkeypatch.setattr("app.web.context.mark_active_menu", lambda menu, path: menu)

    monkeypatch.setattr(
        "app.web.context.build_smart_breadcrumbs",
        lambda menu, request, db: [{"label": "Dashboard"}],
    )

    monkeypatch.setattr("app.web.context.get_flash", lambda request: [])

    ctx = get_template_context(request)

    assert ctx["breadcrumbs"][0]["label"] == "Dashboard"
    assert ctx["page_heading"] == "Dashboard"
    assert ctx["page_title"] == "Dashboard | Aula Robótica"


# =====================================================
# excepción interna -> fallback
# =====================================================


def test_template_context_exception(monkeypatch):
    request = DummyRequest()
    request.state.user = {"sub": "1"}

    monkeypatch.setattr("app.web.context.get_menu_structure", lambda: 1 / 0)

    ctx = get_template_context(request)

    assert ctx["current_user_id"] is None
