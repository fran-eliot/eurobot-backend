# app/modules/auth/auth_service.py
# 🔐 Servicio de autenticación

from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, verify_password
from app.modules.identities.identity_model import Identity
from app.modules.users.user_model import User
from app.modules.users.user_service import get_user_permissions


# =========================================================
# 🪪 BUILD AUTH PAYLOAD (RBAC)
# =========================================================
def build_auth_payload(user):
    """
    Construye el payload estándar para JWT.
    """

    roles = sorted({role.nombre.strip().lower() for role in user.roles})

    permissions = get_user_permissions(user)

    return {
        "sub": str(user.id_usuario),
        "roles": roles,
        "permissions": permissions,
        "username": user.nombre,
        "iat": datetime.now(UTC).timestamp(),
    }


# =========================================================
# 🔄 REFRESH TOKEN → ACCESS TOKEN
# =========================================================
def refresh_access_token(payload: dict, db: Session) -> str:
    """
    Genera un nuevo access token a partir de un refresh token válido.
    """

    # 🔒 Validar tipo de token
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    user_id = int(payload.get("sub"))
    user = db.get(User, user_id)

    if not user or not user.activo:
        raise HTTPException(status_code=403, detail="Usuario no válido o desactivado")

    base_payload = build_auth_payload(user)

    # 🔁 Generar nuevo access token
    return create_access_token({**base_payload, "type": "access"})


# =========================================================
# 🔐 LOGIN (email + password)
# =========================================================
def authenticate_user(db: Session, email: str, password: str) -> dict:
    """
    Autentica un usuario y genera tokens JWT.

    Flujo:
    1. Buscar identidad por email
    2. Validar password
    3. Validar estado usuario
    4. Obtener roles y permisos
    5. Generar tokens
    """

    # =========================================================
    # 🔎 1. BUSCAR IDENTIDAD
    # =========================================================
    identity = db.query(Identity).filter(Identity.email == email).first()

    if not identity:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # =========================================================
    # 🔐 2. VALIDAR PASSWORD
    # =========================================================
    if not identity.password_hash:
        raise HTTPException(
            status_code=401, detail="Login no permitido para este proveedor"
        )

    if not verify_password(password, identity.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # =========================================================
    # 👤 3. VALIDAR USUARIO
    # =========================================================
    user = identity.usuario

    if not user or not user.activo:
        raise HTTPException(status_code=403, detail="Usuario desactivado o inválido")

    # 🎭 4. OBTENER ROLES Y PERMISOS

    payload_base = build_auth_payload(user)

    print("USER ROLES:", [r.nombre.strip().lower() for r in user.roles])

    print("PERMISSIONS GENERADAS:", payload_base["permissions"])

    # =========================================================
    # 🔥 5. TOKENS
    # =========================================================
    access_token = create_access_token({**payload_base, "type": "access"})

    refresh_token = create_refresh_token({**payload_base, "type": "refresh"})

    # =========================================================
    # 📦 6. RESPONSE
    # =========================================================
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,
    }
