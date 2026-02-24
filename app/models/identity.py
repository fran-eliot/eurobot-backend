# app/models/identity.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Identity(Base):
    __tablename__ = "identidades"

    id_identidad = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), nullable=False, unique=True)
    provider = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=True)
    provider_user_id = Column(String(255), nullable=True)

    # FK obligatoria a usuario (participación total)
    user_id = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False
    )

    # FK opcional a rol (rol contextual)
    rol_id = Column(
        Integer,
        ForeignKey("roles.id_rol", ondelete="SET NULL"),
        nullable=True
    )

    # Relaciones ORM
    usuario = relationship("User", back_populates="identidades")
    rol = relationship("Role", back_populates="identidades")

    def __repr__(self):
        return f"<Identity(id={self.id_identidad}, email={self.email})>"
