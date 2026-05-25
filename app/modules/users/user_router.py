# app/modules/users/user_router.py


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.auth_dependencies_api import (
    get_current_user_api,
    require_admin_api,
)
from app.modules.users.user_model import User
from app.modules.users.user_schemas import UserCreate, UserResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description=(
        "Devuelve el listado completo de usuarios. Requiere rol administrador."
    ),
    responses={
        403: {"description": "No tienes permisos suficientes"},
        401: {"description": "Token inválido o expirado"},
    },
)
def get_users(db: Session = Depends(get_db), user=Depends(require_admin_api)):
    return db.query(User).all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description=(
        "Devuelve la información de un usuario específico por su ID."
        "Requiere rol administrador."
    ),
    responses={
        403: {"description": "No tienes permisos suficientes"},
        401: {"description": "Token inválido o expirado"},
        404: {"description": "Usuario no encontrado"},
    },
)
def get_user(
    user_id: int, db: Session = Depends(get_db), user=Depends(require_admin_api)
):
    usuario = db.query(User).filter(User.id_usuario == user_id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return usuario


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener perfil del usuario autenticado",
    description=(
        "Devuelve la información del usuario actualmente autenticado mediante JWT."
    ),
    responses={401: {"description": "Token inválido o expirado"}},
)
def get_my_profile(current_user=Depends(get_current_user_api)):
    return current_user


@router.post(
    "/",
    response_model=UserResponse,
    summary="Crear nuevo usuario",
    description=("Crea un nuevo usuario en el sistema. Requiere rol administrador."),
    responses={
        403: {"description": "No tienes permisos suficientes"},
        401: {"description": "Token inválido o expirado"},
    },
)
def create_user(
    data: UserCreate, db: Session = Depends(get_db), user=Depends(require_admin_api)
):
    nuevo = User(nombre=data.nombre, activo=True)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.delete(
    "/{user_id}",
    summary="Eliminar usuario",
    description=(
        "Elimina un usuario específico por su ID. Requiere rol administrador."
    ),
    responses={
        403: {"description": "No tienes permisos suficientes"},
        401: {"description": "Token inválido o expirado"},
        404: {"description": "Usuario no encontrado"},
    },
)
def delete_user(
    user_id: int, db: Session = Depends(get_db), user=Depends(require_admin_api)
):
    usuario = db.query(User).filter(User.id_usuario == user_id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {"message": "Usuario eliminado correctamente"}
