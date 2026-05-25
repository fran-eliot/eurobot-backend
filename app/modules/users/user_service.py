# app/modules/users/user_service.py

from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.authorization.permissions import has_permission
from app.core.constants.audit_actions import AuditAction
from app.modules.audit.audit_model import AuditLog
from app.modules.audit.audit_service import audit_user_action
from app.modules.identities.identity_model import Identity
from app.modules.roles.role_model import Role
from app.modules.users.user_model import User


# =========================================================
# 👤 ROLES / ACCESO
# =========================================================
def get_user_roles(db: Session, user_id: int) -> list[str]:
    """
    Devuelve los roles asociados a un usuario (vía Identity).
    """

    identity = db.query(Identity).filter(Identity.user_id == user_id).first()

    if identity and identity.rol:
        return [identity.rol.nombre]

    return []


def is_owner(current_user, target_user) -> bool:
    """
    Comprueba si el usuario actual es el propietario del recurso.
    """
    return current_user.id_usuario == target_user.id_usuario


def can_access_user(current_user, target_user, required_permissions: list[str]) -> bool:
    """
    Control de acceso:
    - Permite si es dueño
    - Permite si tiene permisos
    """

    if is_owner(current_user, target_user):
        return True

    return has_permission(current_user.roles_token, required_permissions)


# =========================================================
# 🔎 QUERIES BÁSICAS
# =========================================================
def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id_usuario == user_id).first()


def get_user_or_404(db: Session, user_id: int):
    """
    Devuelve usuario o lanza 404.
    """
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


# =========================================================
# 🔄 CRUD + AUDITORÍA
# =========================================================
def create_user_with_audit(db, nombre, current_user=None, request=None):
    """
    Crea un usuario y registra auditoría.
    """

    user = User(nombre=nombre, activo=True, fecha_creacion=datetime.now(UTC))

    db.add(user)
    db.flush()  # obtener ID sin commit

    if current_user and request:
        audit_user_action(
            db,
            AuditAction.CREATE_USER,
            current_user,
            user,
            request,
            f"Creó usuario {user.nombre}",
        )

    return user


def update_user_with_audit(db, user, new_nombre, current_user=None, request=None):
    """
    Actualiza usuario con auditoría.
    """

    old_nombre = user.nombre
    user.nombre = new_nombre

    if current_user and request:
        audit_user_action(
            db,
            AuditAction.UPDATE_USER,
            current_user,
            user,
            request,
            f"Actualizó usuario {old_nombre} → {new_nombre}",
        )


def delete_user_with_audit(db, user, current_user=None, request=None):
    """
    Elimina usuario con auditoría.
    """

    user_name = user.nombre

    db.delete(user)

    if current_user and request:
        audit_user_action(
            db,
            AuditAction.DELETE_USER,
            current_user,
            user,
            request,
            f"Eliminó usuario {user_name}",
        )


def set_user_active_with_audit(db, user, active: bool, current_user=None, request=None):
    """
    Activa / desactiva usuario con auditoría.
    """

    user.activo = active

    if current_user and request:
        action = AuditAction.ACTIVATE_USER if active else AuditAction.DEACTIVATE_USER

        description = f"{'Activó' if active else 'Desactivó'} usuario {user.nombre}"

        audit_user_action(db, action, current_user, user, request, description)


# =========================================================
# 📜 AUDITORÍA
# =========================================================
def get_user_audit_logs(db: Session, user_id: int, limit: int = 50):
    """
    Devuelve últimos logs asociados al usuario.
    """

    return (
        db.query(AuditLog)
        .filter(AuditLog.resource_type == "user")
        .filter(AuditLog.resource_id == user_id)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )


# =========================================================
# 🔍 BÚSQUEDA / PAGINACIÓN
# =========================================================
def search_users(db, search="", status="all", page=1, per_page=10):
    """
    Búsqueda de usuarios con:
    - texto
    - estado
    - paginación
    """

    query = db.query(User)

    # 🔍 búsqueda por nombre
    if search:
        query = query.filter(User.nombre.ilike(f"%{search}%"))

    # 🎛 filtro estado
    if status == "active":
        query = query.filter(User.activo.is_(True))
    elif status == "inactive":
        query = query.filter(User.activo.is_(False))

    total = query.count()

    users = (
        query.order_by(User.id_usuario.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return users, total


# =========================================================
# 🔐 ROLES
# =========================================================
def sync_user_roles(db, user, role_ids: list[int]):
    """
    Sincroniza roles del usuario.
    """

    user.roles.clear()

    if role_ids:
        roles = db.query(Role).filter(Role.id_rol.in_(role_ids)).all()

        user.roles.extend(roles)


# =========================================================
# 🔐 PERMISOS
# =========================================================
def get_user_permissions(user):
    """
    Devuelve permisos efectivos (sin duplicados).
    """

    print(f"Obteniendo permisos para usuario {user.nombre} (ID: {user.id_usuario})")

    for role in user.roles:
        print(f"ROL: {role.nombre}")
        for perm in role.permissions:
            print(f"  - PERMISO: {perm.nombre}")

    return sorted(
        {
            perm.nombre.strip().lower()
            for role in user.roles
            for perm in role.permissions
        }
    )


def get_user_permissions_by_role(user):
    """
    Devuelve permisos agrupados por rol.
    """

    result = []

    for role in user.roles:
        perms = []

        for p in role.permissions:
            module, action = p.nombre.split(":")
            perms.append({"module": module, "action": action})

        result.append({"role": role, "permissions": perms})

    return result


def get_user_permissions_with_origin(user):
    """
    Devuelve permisos con el rol que los otorga.
    """

    permissions_map = {}

    for role in user.roles:
        for perm in role.permissions:
            permissions_map.setdefault(perm.nombre, []).append(role.nombre)

    result = []

    for perm_name, roles in permissions_map.items():
        module, action = perm_name.split(":")

        result.append(
            {"name": perm_name, "module": module, "action": action, "roles": roles}
        )

    return sorted(result, key=lambda x: x["module"])


# =========================================================
# 🧠 EXPLICACIÓN DE PERMISOS
# =========================================================
def explain_user_permission(user, action: str, target=None):
    """
    Explica si un usuario puede realizar una acción y por qué.
    """

    roles = [r.nombre for r in user.roles]
    user_id = getattr(user, "id_usuario", None)

    # 🔥 ADMIN override
    if "admin" in roles:
        return {"allowed": True, "reason": "admin", "roles": roles}

    # 🔥 ownership
    if target and getattr(target, "id_usuario", None) == user_id:
        if action in ["view", "edit"]:
            return {"allowed": True, "reason": "owner", "roles": roles}

    # 🔐 mapping acción → permiso
    action_map = {
        "view": "users:read",
        "edit": "users:update",
        "delete": "users:delete",
        "create": "users:create",
    }

    required_perm = action_map.get(action)

    roles_with_permission = [
        role.nombre
        for role in user.roles
        for perm in role.permissions
        if perm.nombre == required_perm
    ]

    if roles_with_permission:
        return {
            "allowed": True,
            "reason": "permission",
            "permission": required_perm,
            "roles": roles_with_permission,
        }

    return {
        "allowed": False,
        "reason": "missing_permission",
        "permission": required_perm,
        "roles": roles,
    }
