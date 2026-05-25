# app/modules/users/user_role_model.py
# 🔗 Tabla intermedia User ↔ Role (many-to-many)

from sqlalchemy import Column, ForeignKey, Integer

from app.db.base import Base


class UserRole(Base):
    """
    Tabla intermedia que relaciona usuarios con roles.

    Representa una relación many-to-many:
    - Un usuario puede tener múltiples roles
    - Un rol puede pertenecer a múltiples usuarios

    ⚠️ No contiene lógica de negocio.
    Solo define la relación en base de datos.
    """

    __tablename__ = "user_rol"

    # =========================================================
    # 🔑 FOREIGN KEYS
    # =========================================================

    user_id = Column(
        Integer,
        ForeignKey(
            "usuarios.id_usuario",
            ondelete="CASCADE",  # si se elimina usuario → borra relaciones
        ),
        primary_key=True,
        index=True,
    )

    rol_id = Column(
        Integer,
        ForeignKey(
            "roles.id_rol",
            ondelete="CASCADE",  # si se elimina rol → borra relaciones
        ),
        primary_key=True,
        index=True,
    )

    # =========================================================
    # 🧠 NOTAS DE DISEÑO
    # =========================================================
    """
    ✔ Clave primaria compuesta (user_id, rol_id)
        → evita duplicados automáticamente

    ✔ No se define id autoincremental
        → es una tabla de relación pura

    ✔ No se añaden timestamps (por ahora)
        → mantener simple hasta que lo necesites

    ✔ Usada como:
        secondary=UserRole.__table__

    👉 Si en el futuro necesitas:
        - auditoría de asignación de roles
        - fechas (created_at)
        - quién asignó el rol

    entonces deberías convertirla en entidad completa.
    """

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, rol_id={self.rol_id})>"
