# app/modules/roles/role_service.py
# 🔐 Lógica de negocio para Roles y Permisos (RBAC)

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.audit.audit_model import AuditLog
from app.modules.roles.role_model import Permission, Role


# =========================================================
# 🧑‍💼 ROLES
# =========================================================
def get_all_roles(db: Session) -> list[Role]:
    """
    Devuelve todos los roles ordenados por nombre.
    """
    return db.query(Role).order_by(Role.nombre).all()


def get_role_by_id(db: Session, role_id: int) -> Role | None:
    """
    Devuelve un rol por ID o None.
    """
    return db.query(Role).filter(Role.id_rol == role_id).first()


def get_role_or_404(db: Session, role_id: int) -> Role:
    """
    Devuelve un rol o lanza 404 si no existe.
    """
    role = get_role_by_id(db, role_id)

    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return role


def create_role(db: Session, nombre: str, descripcion: str | None = None) -> Role:
    """
    Crea un nuevo rol.
    """

    # 🔥 evitar duplicados
    existing = db.query(Role).filter(Role.nombre == nombre).first()

    if existing:
        raise HTTPException(status_code=400, detail="El rol ya existe")

    role = Role(nombre=nombre.strip().lower(), descripcion=descripcion)

    db.add(role)
    db.flush()  # necesario para obtener ID

    return role


def update_role(db: Session, role: Role, nombre: str, descripcion: str | None = None):
    """
    Actualiza un rol existente.
    """

    # 🔥 evitar duplicados (otro rol con mismo nombre)
    existing = (
        db.query(Role).filter(Role.nombre == nombre, Role.id_rol != role.id_rol).first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")

    role.nombre = nombre.strip().lower()
    role.descripcion = descripcion


def delete_role(db: Session, role: Role):
    """
    Elimina un rol.
    """
    db.delete(role)


# =========================================================
# 🔑 PERMISOS
# =========================================================
def get_all_permissions(db: Session) -> list[Permission]:
    """
    Devuelve todos los permisos ordenados por nombre.
    """
    return db.query(Permission).order_by(Permission.nombre).all()


def sync_role_permissions(db: Session, role: Role, permission_ids: list[int]):
    """
    Sincroniza los permisos de un rol (replace completo).
    """

    # 🔥 limpiar permisos actuales
    role.permissions.clear()

    if not permission_ids:
        return

    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()

    role.permissions.extend(permissions)


def group_permissions(permissions: list[Permission]) -> dict:
    """
    Agrupa permisos por módulo para UI.

    Ejemplo:
    {
        "users": [
            {"id": 1, "name": "users:read", "action": "read"},
            {"id": 2, "name": "users:create", "action": "create"}
        ]
    }
    """

    grouped: dict[str, list] = {}

    for perm in permissions:
        try:
            module, action = perm.nombre.split(":")
        except ValueError:
            # fallback por si hay permisos mal formados
            module = "other"
            action = perm.nombre

        grouped.setdefault(module, []).append(
            {"id": perm.id, "name": perm.nombre, "action": action}
        )

    # 🔥 ordenar acciones dentro de cada módulo
    for module in grouped:
        grouped[module].sort(key=lambda x: x["action"])

    return grouped


# =========================================================
# 📜 AUDITORÍA
# =========================================================
def get_role_audit_logs(db: Session, role_id: int, limit: int = 20):
    """
    Devuelve historial de cambios de un rol.
    """

    return (
        db.query(AuditLog)
        .filter(AuditLog.resource_type == "role", AuditLog.resource_id == role_id)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )
