# tests/test_role_service.py

# Este archivo contiene pruebas para la funcionalidad del servicio de roles.
# Se definen pruebas para verificar que las funciones del servicio de roles
# funcionan correctamente, como la creación, actualización, eliminación y sincronización
# de permisos de roles, así como la agrupación de permisos.

from fastapi import HTTPException

from app.modules.roles.role_model import Permission, Role
from app.modules.roles.role_service import (
    create_role,
    delete_role,
    get_role_or_404,
    group_permissions,
    sync_role_permissions,
    update_role,
)


def test_get_role_or_404_ok(db):
    role = Role(nombre="tester")
    db.add(role)
    db.commit()

    found = get_role_or_404(db, role.id_rol)

    assert found.nombre == "tester"


def test_get_role_or_404_fail(db):
    try:
        get_role_or_404(db, 999)
        assert False
    except HTTPException as e:
        assert e.status_code == 404


def test_create_role_ok(db):
    role = create_role(db, "nuevo", "Rol nuevo")
    db.commit()

    assert role.id_rol is not None
    assert role.nombre == "nuevo"


def test_create_role_duplicate(db):
    try:
        create_role(db, "admin")
        assert False
    except HTTPException as e:
        assert e.status_code == 400


def test_update_role_ok(db):
    role = Role(nombre="old")
    db.add(role)
    db.commit()

    update_role(db, role, "new", "desc")

    assert role.nombre == "new"


def test_update_role_duplicate(db):
    r1 = Role(nombre="uno")
    r2 = Role(nombre="dos")

    db.add_all([r1, r2])
    db.commit()

    try:
        update_role(db, r2, "uno")
        assert False
    except HTTPException as e:
        assert e.status_code == 400


def test_sync_role_permissions(db):
    role = Role(nombre="permrole")
    db.add(role)
    db.commit()

    p1 = db.query(Permission).filter_by(nombre="users:read").first()
    p2 = db.query(Permission).filter_by(nombre="users:update").first()

    sync_role_permissions(db, role, [p1.id, p2.id])

    assert len(role.permissions) == 2


def test_group_permissions(db):
    perms = [
        Permission(nombre="users:read"),
        Permission(nombre="users:update"),
        Permission(nombre="roles:delete"),
    ]

    grouped = group_permissions(perms)

    assert "users" in grouped
    assert "roles" in grouped
    assert len(grouped["users"]) == 2


def test_delete_role(db):
    role = Role(nombre="temp")
    db.add(role)
    db.commit()

    delete_role(db, role)
    db.commit()

    assert db.query(Role).filter_by(nombre="temp").first() is None
