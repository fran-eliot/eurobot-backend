# app/modules/identities/identity_model.py
# 🔐 Modelo de identidad (credenciales de autenticación)

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Identity(Base):
    """
    Representa una identidad de autenticación de un usuario.

    Permite:
    - Login local (email + password)
    - Login federado (Google, GitHub, etc.)

    Un usuario puede tener múltiples identidades.
    """

    __tablename__ = "identities"

    # =========================================================
    # 🆔 PRIMARY KEY
    # =========================================================
    id = Column(Integer, primary_key=True)

    # =========================================================
    # 📧 CREDENCIALES
    # =========================================================
    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(
        String(255),
        nullable=True,  # null si es login externo (OAuth)
    )

    provider = Column(
        String(50),
        default="local",
        nullable=False,
        # ejemplos: local, google, github
    )

    # =========================================================
    # 🔗 RELACIÓN CON USUARIO
    # =========================================================
    user_id = Column(
        Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False
    )

    usuario = relationship("User", back_populates="identidades")

    # =========================================================
    # 🧾 REPRESENTACIÓN
    # =========================================================
    def __repr__(self):
        return f"<Identity(id={self.id}, email={self.email}, provider={self.provider})>"
