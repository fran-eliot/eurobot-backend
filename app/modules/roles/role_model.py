# app/modules/roles/role_model.py
# 🔐 Modelo de Roles y Permisos (RBAC)

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.modules.users.user_role_model import UserRole


# =========================================================
# 🔑 PERMISSION
# =========================================================
class Permission(Base):
    """
    Representa una acción del sistema.
    Ejemplo: users:read, users:create, roles:update
    """

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)

    # nombre único del permiso (formato: módulo:acción)
    nombre = Column(String(100), unique=True, nullable=False)

    # 🔗 relación inversa con roles (many-to-many)
    roles = relationship(
        "Role",
        secondary="role_permissions",  # tabla intermedia
        back_populates="permissions",
        lazy="selectin",  # ⚡ optimización de carga
    )

    def __repr__(self):
        return f"<Permission(nombre={self.nombre})>"


# =========================================================
# 🧑‍💼 ROLE
# =========================================================
class Role(Base):
    """
    Representa un rol del sistema.
    Ejemplo: admin, profesor, estudiante
    """

    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)

    # nombre único del rol
    nombre = Column(String(100), unique=True, nullable=False)

    # descripción opcional (útil para UI/admin)
    descripcion = Column(String(255), nullable=True)

    # 🔗 relación con usuarios (many-to-many)
    usuarios = relationship(
        "User", secondary=UserRole.__table__, back_populates="roles", lazy="selectin"
    )

    # 🔗 relación con permisos (many-to-many)
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Role(nombre={self.nombre})>"


# =========================================================
# 🔗 ROLE ↔ PERMISSION (tabla intermedia)
# =========================================================
class RolePermission(Base):
    """
    Tabla pivote many-to-many entre roles y permisos.
    """

    __tablename__ = "role_permissions"

    role_id = Column(
        Integer, ForeignKey("roles.id_rol", ondelete="CASCADE"), primary_key=True
    )

    permission_id = Column(
        Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )
