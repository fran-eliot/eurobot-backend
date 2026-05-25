# app/modules/auth/auth_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.auth_schemas import LoginRequest
from app.modules.auth.auth_service import authenticate_user

router = APIRouter()


@router.post(
    "/login",
    openapi_extra={"security": []},
    summary="Iniciar sesión, autenticación de usuario",
    description=(
        "Autentica una identidad y devuelve un token JWt"
        "válido para acceder a los endpoints protegidos."
    ),
    responses={
        200: {"description": "Inicio de sesión exitoso, devuelve token JWT"},
        401: {"description": "Credenciales inválidas o usuario desactivado"},
    },
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, data.email, data.password)
