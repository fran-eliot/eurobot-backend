# tests/test_user_service_extra.py
# Este archivo contiene pruebas adicionales para el servicio de usuarios,
# incluyendo la obtención de roles de usuario, la verificación de acceso a usuarios,
# la eliminación de usuarios con auditoría, la obtención de registros de auditoría
# de usuarios, y la explicación de permisos de usuario.


from app.modules.roles.role_model import Permission, Role
from app.modules.users.user_model import User
from app.modules.users.user_service import (
    can_access_user,
    delete_user_with_audit,
    explain_user_permission,
    get_user_audit_logs,
    get_user_permissions_by_role,
    get_user_permissions_with_origin,
    get_user_roles,
)


class DummyRequest:
    class Client:
        host = "127.0.0.1"

    client = Client()
    headers = {"user-agent": "pytest"}


def test_get_user_roles(db):
    roles = get_user_roles(db, 9999)
    assert roles == []


def test_can_access_user_owner(db):
    user = db.query(User).filter(User.nombre == "Admin Principal").first()

    assert (
        can_access_user(
            current_user=user, target_user=user, required_permissions=["users:delete"]
        )
        is True
    )


def test_delete_user_with_audit(db):
    current_user = db.query(User).filter(User.nombre == "Admin Principal").first()

    target = User(nombre="Temporal", activo=True)
    db.add(target)
    db.commit()

    delete_user_with_audit(
        db, target, current_user=current_user, request=DummyRequest()
    )
    db.commit()

    deleted = db.query(User).filter(User.nombre == "Temporal").first()
    assert deleted is None


def test_get_user_audit_logs(db):
    current_user = db.query(User).filter(User.nombre == "Admin Principal").first()

    target = User(nombre="Audit Target", activo=True)
    db.add(target)
    db.commit()

    delete_user_with_audit(
        db, target, current_user=current_user, request=DummyRequest()
    )
    db.commit()

    logs = get_user_audit_logs(db, target.id_usuario)
    assert isinstance(logs, list)


def test_get_user_permissions_by_role(db):
    perm = Permission(nombre="qa:read")
    role = Role(nombre="qa_role")
    role.permissions.append(perm)

    user = User(nombre="QA User", activo=True)
    user.roles.append(role)

    db.add_all([perm, role, user])
    db.commit()

    result = get_user_permissions_by_role(user)

    assert result[0]["role"].nombre == "qa_role"
    assert result[0]["permissions"][0]["module"] == "qa"


def test_get_user_permissions_with_origin(db):
    perm = Permission(nombre="editor:update")
    role = Role(nombre="editor_role")
    role.permissions.append(perm)

    user = User(nombre="Editor", activo=True)
    user.roles.append(role)

    db.add_all([perm, role, user])
    db.commit()

    result = get_user_permissions_with_origin(user)

    assert result[0]["name"] == "editor:update"
    assert "editor_role" in result[0]["roles"]


def test_explain_user_permission_owner(db):
    user = User(nombre="Owner", activo=True)
    db.add(user)
    db.commit()

    result = explain_user_permission(user=user, action="view", target=user)

    assert result["allowed"] is True
    assert result["reason"] == "owner"
