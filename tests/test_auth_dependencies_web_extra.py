# tests/test_auth_dependencies_web_extra.py
# Este archivo contiene pruebas para las dependencias de autenticación y
# autorización específicas de la interfaz web. Se prueban casos como la
# obtención del usuario actual desde el token, la verificación de roles y
# permisos, y las combinaciones de propietario/permiso para acciones sensibles.
# Se utilizan técnicas de monkeypatching para simular comportamientos y estados
# específicos en las pruebas.

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.modules.auth.auth_dependencies_web import (
    get_current_user_web,
    require_owner_or_permission_web,
    require_permission_and_not_self_web,
    require_permission_web,
    require_roles_web,
)
from app.modules.users.user_model import User

# =========================================================
# HELPERS
# =========================================================


def make_request(payload=None):
    return SimpleNamespace(state=SimpleNamespace(user=payload))


# =========================================================
# get_current_user_web
# =========================================================


def test_get_current_user_web_without_payload(db):
    request = make_request(None)

    with pytest.raises(HTTPException) as exc:
        get_current_user_web(request, db)

    assert exc.value.status_code == 401
    assert "No autenticado" in exc.value.detail


def test_get_current_user_web_without_sub(db):
    request = make_request({"roles": ["admin"], "permissions": []})

    with pytest.raises(HTTPException) as exc:
        get_current_user_web(request, db)

    assert exc.value.status_code == 401
    assert "Token inválido" in exc.value.detail


def test_get_current_user_web_user_not_found(db):
    request = make_request({"sub": 999, "roles": ["admin"], "permissions": []})

    with pytest.raises(HTTPException) as exc:
        get_current_user_web(request, db)

    assert exc.value.status_code == 401
    assert "Usuario no encontrado" in exc.value.detail


def test_get_current_user_web_ok(db):
    request = make_request(
        {"sub": 1, "roles": ["admin"], "permissions": ["users:read"]}
    )

    user = get_current_user_web(request, db)

    assert user.id_usuario == 1
    assert user.roles_token == ["admin"]
    assert "users:read" in user.permissions


# =========================================================
# require_roles_web
# =========================================================


def test_require_roles_web_ok():
    checker = require_roles_web("admin")

    user = SimpleNamespace(roles_token=["admin"])

    result = checker(user)

    assert result == user


def test_require_roles_web_forbidden():
    checker = require_roles_web("admin")

    user = SimpleNamespace(roles_token=["student"])

    with pytest.raises(HTTPException) as exc:
        checker(user)

    assert exc.value.status_code == 403


# =========================================================
# require_permission_web
# =========================================================


def test_require_permission_web_ok():
    checker = require_permission_web("users", "read")

    user = SimpleNamespace(permissions=["users:read", "roles:read"])

    result = checker(user)

    assert result == user


def test_require_permission_web_forbidden():
    checker = require_permission_web("users", "delete")

    user = SimpleNamespace(permissions=["users:read"])

    with pytest.raises(HTTPException) as exc:
        checker(user)

    assert exc.value.status_code == 403


def test_require_permission_web_without_permissions_attr():
    checker = require_permission_web("users", "read")

    user = SimpleNamespace()

    with pytest.raises(HTTPException) as exc:
        checker(user)

    assert exc.value.status_code == 403


# =========================================================
# require_owner_or_permission_web
# =========================================================


def test_require_owner_or_permission_web_ok(monkeypatch, db):
    checker = require_owner_or_permission_web("users", "read")

    fake_target = User(id_usuario=2, nombre="Alumno", activo=True)

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.get_user_or_404",
        lambda db, user_id: fake_target,
    )

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.can_user_action",
        lambda action, resource, current_user, target_user: True,
    )

    current_user = SimpleNamespace(id_usuario=1)

    result = checker(2, db, current_user)

    assert result == fake_target


def test_require_owner_or_permission_web_forbidden(monkeypatch, db):
    checker = require_owner_or_permission_web("users", "read")

    fake_target = User(id_usuario=2, nombre="Alumno", activo=True)

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.get_user_or_404",
        lambda db, user_id: fake_target,
    )

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.can_user_action",
        lambda action, resource, current_user, target_user: False,
    )

    current_user = SimpleNamespace(id_usuario=1)

    with pytest.raises(HTTPException) as exc:
        checker(2, db, current_user)

    assert exc.value.status_code == 403


# =========================================================
# require_permission_and_not_self_web
# =========================================================


def test_require_permission_and_not_self_self_forbidden(monkeypatch, db):
    checker = require_permission_and_not_self_web("users", "delete")

    fake_target = User(id_usuario=1, nombre="Admin", activo=True)

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.get_user_or_404",
        lambda db, user_id: fake_target,
    )

    current_user = SimpleNamespace(id_usuario=1)

    with pytest.raises(HTTPException) as exc:
        checker(1, db, current_user)

    assert exc.value.status_code == 403
    assert "ti mismo" in exc.value.detail


def test_require_permission_and_not_self_no_permission(monkeypatch, db):
    checker = require_permission_and_not_self_web("users", "delete")

    fake_target = User(id_usuario=2, nombre="Alumno", activo=True)

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.get_user_or_404",
        lambda db, user_id: fake_target,
    )

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.can_user_action",
        lambda action, resource, current_user, target_user: False,
    )

    current_user = SimpleNamespace(id_usuario=1)

    with pytest.raises(HTTPException) as exc:
        checker(2, db, current_user)

    assert exc.value.status_code == 403


def test_require_permission_and_not_self_ok(monkeypatch, db):
    checker = require_permission_and_not_self_web("users", "delete")

    fake_target = User(id_usuario=2, nombre="Alumno", activo=True)

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.get_user_or_404",
        lambda db, user_id: fake_target,
    )

    monkeypatch.setattr(
        "app.modules.auth.auth_dependencies_web.can_user_action",
        lambda action, resource, current_user, target_user: True,
    )

    current_user = SimpleNamespace(id_usuario=1)

    result = checker(2, db, current_user)

    assert result == current_user
