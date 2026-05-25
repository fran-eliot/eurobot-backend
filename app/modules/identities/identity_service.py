# app/modules/identities/identity_service.py
# 🔐 Lógica de negocio para identidades (auth layer)

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.identities.identity_model import Identity


# =========================================================
# 📋 QUERIES BÁSICAS
# =========================================================
def get_all_identities(db: Session):
    """
    Devuelve todas las identidades.
    """
    return db.query(Identity).all()


def get_identity_by_id(db: Session, identity_id: int):
    """
    Obtiene una identidad por ID.
    """
    return db.query(Identity).filter(Identity.id == identity_id).first()


def get_identity_or_404(db: Session, identity_id: int):
    """
    Obtiene una identidad o lanza 404 si no existe.
    """
    identity = get_identity_by_id(db, identity_id)

    if not identity:
        raise HTTPException(status_code=404, detail="Identidad no encontrada")

    return identity


# =========================================================
# ➕ CREATE
# =========================================================
def create_identity(
    db: Session, email: str, password: str, user_id: int, provider: str = "local"
):
    """
    Crea una nueva identidad.

    Incluye:
    - validación de email único
    - hash de contraseña
    - 🔥 sincronización RBAC (user.roles)
    """

    # 🔎 1. Email único
    existing = db.query(Identity).filter(Identity.email == email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # 🔐 2. Crear identidad
    identity = Identity(
        email=email,
        password_hash=hash_password(password),
        user_id=user_id,
        provider=provider,
    )

    db.add(identity)
    db.flush()

    return identity


# =========================================================
# ✏️ UPDATE
# =========================================================
def update_identity(
    db: Session,
    identity: Identity,
    email: str,
    user_id: int,
    provider: str,
    password: str | None = None,
):
    """
    Actualiza una identidad existente.

    - Permite cambio de email, usuario y provider
    - Password opcional (solo si se envía)
    """

    identity.email = email
    identity.user_id = user_id
    identity.provider = provider

    # 🔐 actualización de password opcional
    if password:
        identity.password_hash = hash_password(password)


# =========================================================
# ❌ DELETE
# =========================================================
def delete_identity(db: Session, identity: Identity):
    """
    Elimina una identidad.
    """
    db.delete(identity)
