# tests/test_auth_service.py
# Este archivo contiene pruebas para el servicio de autenticación de la aplicación.


import pytest
from fastapi import HTTPException

from app.core.security import hash_password
from app.modules.auth.auth_service import (
    authenticate_user,
    build_auth_payload,
    refresh_access_token,
)
from app.modules.identities.identity_model import Identity
from app.modules.roles.role_model import Role
from app.modules.users.user_model import User


def test_build_auth_payload(db):
    role = Role(nombre="manager")
    user = User(nombre="Fran", activo=True)
    user.roles.append(role)

    db.add_all([role, user])
    db.commit()

    payload = build_auth_payload(user)

    assert payload["sub"] == str(user.id_usuario)
    assert payload["username"] == "Fran"
    assert "roles" in payload
    assert "permissions" in payload
    assert "iat" in payload


def test_authenticate_user_ok(db):
    user = User(nombre="Login User", activo=True)
    db.add(user)
    db.flush()

    identity = Identity(
        email="login@test.com",
        password_hash=hash_password("1234"),
        user_id=user.id_usuario,
    )
    db.add(identity)
    db.commit()

    result = authenticate_user(db, "login@test.com", "1234")

    assert "access_token" in result
    assert "refresh_token" in result
    assert result["user"].nombre == "Login User"


def test_authenticate_user_wrong_email(db):
    with pytest.raises(HTTPException) as exc:
        authenticate_user(db, "none@test.com", "1234")

    assert exc.value.status_code == 401


def test_authenticate_user_wrong_password(db):
    user = User(nombre="User", activo=True)
    db.add(user)
    db.flush()

    identity = Identity(
        email="wrong@test.com",
        password_hash=hash_password("1234"),
        user_id=user.id_usuario,
    )
    db.add(identity)
    db.commit()

    with pytest.raises(HTTPException) as exc:
        authenticate_user(db, "wrong@test.com", "bad")

    assert exc.value.status_code == 401


def test_authenticate_user_disabled(db):
    user = User(nombre="Off", activo=False)
    db.add(user)
    db.flush()

    identity = Identity(
        email="off@test.com",
        password_hash=hash_password("1234"),
        user_id=user.id_usuario,
    )
    db.add(identity)
    db.commit()

    with pytest.raises(HTTPException) as exc:
        authenticate_user(db, "off@test.com", "1234")

    assert exc.value.status_code == 403


def test_refresh_access_token_ok(db):
    user = User(nombre="Refresh", activo=True)
    db.add(user)
    db.commit()

    payload = {"sub": str(user.id_usuario), "type": "refresh"}

    token = refresh_access_token(payload, db)
    assert isinstance(token, str)


def test_refresh_access_token_bad_type(db):
    with pytest.raises(HTTPException) as exc:
        refresh_access_token({"type": "access", "sub": "1"}, db)

    assert exc.value.status_code == 401


def test_refresh_access_token_user_not_found(db):
    with pytest.raises(HTTPException) as exc:
        refresh_access_token({"type": "refresh", "sub": "999"}, db)

    assert exc.value.status_code == 403
