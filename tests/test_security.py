# tests/test_security.py

# Este archivo contiene pruebas para la funcionalidad de seguridad,
# incluyendo el hashing de contraseñas,
# la verificación de contraseñas, la creación de tokens de acceso y actualización,
# y la decodificación de tokens. Se definen pruebas para verificar que estas funciones

import pytest
from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    hashed = hash_password("1234")

    assert hashed != "1234"
    assert isinstance(hashed, str)


def test_verify_password_ok():
    hashed = hash_password("1234")

    assert verify_password("1234", hashed) is True


def test_verify_password_fail():
    hashed = hash_password("1234")

    assert verify_password("wrong", hashed) is False


def test_create_access_token():
    token = create_access_token({"sub": "1", "roles": ["admin"]})

    assert isinstance(token, str)
    assert len(token) > 20


def test_create_refresh_token():
    token = create_refresh_token({"sub": "1"})

    assert isinstance(token, str)


def test_decode_token_ok():
    token = create_access_token({"sub": "99", "roles": ["student"]})

    payload = decode_token(token)

    assert payload["sub"] == "99"


def test_decode_token_invalid():
    with pytest.raises(HTTPException) as exc:
        decode_token("token.fake.invalid")

    assert exc.value.status_code == 401
