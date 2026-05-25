# tests/test_security_extra.py
# Este archivo contiene pruebas adicionales para la funcionalidad de seguridad,
# específicamente para validar que los tokens de acceso y refresh sean del tipo
# correcto. Se verifica que si se intenta validar un token con el tipo incorrecto,
# se lance una excepción HTTP 401 con el mensaje adecuado.

import pytest
from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    create_refresh_token,
    validate_access_token,
    validate_refresh_token,
)


def test_validate_access_token_wrong_type():
    token = create_refresh_token({"sub": "1"})

    with pytest.raises(HTTPException) as exc:
        validate_access_token(token)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Token de acceso inválido"


def test_validate_refresh_token_wrong_type():
    token = create_access_token({"sub": "1"})

    with pytest.raises(HTTPException) as exc:
        validate_refresh_token(token)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Refresh token inválido"
