# tests/test_permissions_core.py
# Este archivo contiene pruebas para la funcionalidad de permisos en el núcleo de la
# aplicación.


from types import SimpleNamespace

from app.core.authorization.permissions import (
    can_access_resource,
    get_permissions_from_roles,
    has_permission,
    has_permission_from_roles,
)
from app.core.authorization.role_permissions import ROLE_PERMISSIONS


def test_has_permission_ok():
    assert has_permission(["Users:Read", "roles:update"], ["users:read"]) is True


def test_has_permission_fail_empty():
    assert has_permission([], ["users:read"]) is False


def test_has_permission_any_match():
    assert has_permission(["roles:read"], ["users:read", "roles:read"]) is True


def test_has_permission_from_roles_admin():
    # coger un rol que tenga permisos definidos
    role = next(iter(ROLE_PERMISSIONS.keys()))
    perms = ROLE_PERMISSIONS[role]

    if "*" in perms:
        assert has_permission_from_roles([role], ["anything:anything"]) is True
    else:
        # si no tiene *, probamos con uno real
        if perms:
            assert has_permission_from_roles([role], [perms[0]]) is True


def test_has_permission_from_roles_match():
    role = next(iter(ROLE_PERMISSIONS.keys()))
    perms = ROLE_PERMISSIONS[role]

    if perms:
        assert has_permission_from_roles([role], [perms[0]]) is True


def test_has_permission_from_roles_fail():
    assert has_permission_from_roles(["student"], ["users:delete"]) is False


def test_get_permissions_from_roles_empty():
    assert get_permissions_from_roles([]) == []


def test_get_permissions_from_roles_admin():
    role = next(iter(ROLE_PERMISSIONS.keys()))
    perms = ROLE_PERMISSIONS[role]

    result = get_permissions_from_roles([role])

    if "*" in perms:
        assert result == ["*"]
    else:
        assert set(result) == set(perms)


def test_get_permissions_from_roles_normal():
    role = next(iter(ROLE_PERMISSIONS.keys()))
    perms = ROLE_PERMISSIONS[role]

    result = get_permissions_from_roles([role])

    for p in perms:
        assert p in result


def test_can_access_resource_owner():
    user = SimpleNamespace(id_usuario=1, permissions=[])
    assert can_access_resource(user, 1, ["users:read"]) is True


def test_can_access_resource_by_permission():
    user = SimpleNamespace(id_usuario=2, permissions=["users:read"])
    assert can_access_resource(user, 1, ["users:read"]) is True


def test_can_access_resource_denied():
    user = SimpleNamespace(id_usuario=2, permissions=["dashboard:read"])
    assert can_access_resource(user, 1, ["users:read"]) is False
