# tests/test_user_service.py

# Este archivo contiene pruebas para la funcionalidad del servicio de usuarios.
# Se definen pruebas para verificar que las funciones del servicio de usuarios
# funcionan correctamente, como la creación, actualización, búsqueda y sincronización
# de roles de usuarios, así como la obtención de permisos y explicación de permisos.


from fastapi import HTTPException

from app.modules.roles.role_model import Permission, Role
from app.modules.users.user_model import User
from app.modules.users.user_service import (
    create_user_with_audit,
    explain_user_permission,
    get_user_or_404,
    get_user_permissions,
    search_users,
    set_user_active_with_audit,
    sync_user_roles,
    update_user_with_audit,
)


def test_get_user_or_404_ok(db):
    user = User(nombre="Test User", activo=True)
    db.add(user)
    db.commit()

    found = get_user_or_404(db, user.id_usuario)

    assert found.nombre == "Test User"


def test_get_user_or_404_fail(db):
    try:
        get_user_or_404(db, 999)
        assert False
    except HTTPException as e:
        assert e.status_code == 404


def test_create_user_with_audit(db):
    user = create_user_with_audit(db, "Nuevo Usuario")
    db.commit()

    assert user.id_usuario is not None
    assert user.nombre == "Nuevo Usuario"
    assert user.activo is True


def test_update_user_with_audit(db):
    user = User(nombre="Viejo", activo=True)
    db.add(user)
    db.commit()

    update_user_with_audit(db, user, "Nuevo")

    assert user.nombre == "Nuevo"


def test_set_user_active_false(db):
    user = User(nombre="Activo", activo=True)
    db.add(user)
    db.commit()

    set_user_active_with_audit(db, user, False)

    assert user.activo is False


def test_search_users_text(db):
    db.add_all(
        [
            User(nombre="Laura", activo=True),
            User(nombre="Carlos", activo=True),
        ]
    )
    db.commit()

    users, total = search_users(db, search="Lau")

    assert total == 1
    assert users[0].nombre == "Laura"


def test_search_users_active(db):
    db.add_all(
        [
            User(nombre="Activo", activo=True),
            User(nombre="Inactivo", activo=False),
        ]
    )
    db.commit()

    users, total = search_users(db, status="active")

    assert total >= 1
    assert all(u.activo for u in users)


def test_sync_user_roles(db):
    user = User(nombre="Usuario Rol", activo=True)
    role = Role(nombre="tester")

    db.add_all([user, role])
    db.commit()

    sync_user_roles(db, user, [role.id_rol])

    assert len(user.roles) == 1
    assert user.roles[0].nombre == "tester"


def test_get_user_permissions(db):
    perm = db.query(Permission).filter_by(nombre="users:read").first()

    role = Role(nombre="perm_role_test")
    role.permissions.append(perm)

    user = User(nombre="Perm User", activo=True)
    user.roles.append(role)

    db.add_all([role, user])
    db.commit()

    perms = get_user_permissions(user)

    assert "users:read" in perms


def test_explain_permission_admin(db):
    role = Role(nombre="admin")
    user = User(nombre="Admin", activo=True)
    user.roles.append(role)

    result = explain_user_permission(user, "delete")

    assert result["allowed"] is True
    assert result["reason"] == "admin"


def test_explain_permission_missing(db):
    role = Role(nombre="student")
    user = User(nombre="Alumno", activo=True)
    user.roles.append(role)

    result = explain_user_permission(user, "delete")

    assert result["allowed"] is False
    assert result["reason"] == "missing_permission"
