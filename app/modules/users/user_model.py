# app/modules/users/user_model.py
# 👤 Modelo de Usuario (núcleo del sistema)

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.modules.users.user_role_model import UserRole


class User(Base):
    """
    Modelo principal de usuario.

    Representa a una persona dentro del sistema.
    No contiene credenciales (eso va en Identity).
    """

    __tablename__ = "usuarios"

    # =========================================================
    # 🔑 CAMPOS
    # =========================================================

    id_usuario = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre = Column(
        String(150),
        nullable=False
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=False
    )

    fecha_creacion = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    # =========================================================
    # 🔗 RELACIONES
    # =========================================================

    # 🔐 Identidades (login, email, provider...)
    identidades = relationship(
        "Identity",
        back_populates="usuario",
        cascade="all, delete",
        passive_deletes=True
    )

    # 🛡 Roles (RBAC many-to-many)
    roles = relationship(
        "Role",
        secondary=UserRole.__table__,
        back_populates="usuarios"
    )

    # 🧾 Auditoría
    audit_logs = relationship(
        "AuditLog",
        back_populates="user"
    )

    # 🧑‍💻 Tareas asignadas
    activities = relationship(
        "Activity",
        back_populates="user"
    )

    # Notificaciones
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    #Adjuntos subidos por el usuario
    activity_attachments = relationship(
        "ActivityAttachment",
        back_populates="uploader",
    )

    # =========================================================
    # 🧠 HELPERS (ligeros, sin lógica de negocio pesada)
    # =========================================================

    def is_active(self) -> bool:
        """
        Indica si el usuario está activo.
        """
        return self.activo

    def __repr__(self):
        return f"<User(id={self.id_usuario}, nombre='{self.nombre}')>"