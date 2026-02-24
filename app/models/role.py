# app/models/role.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    # Relación N:M con User
    usuarios = relationship(
        "User",
        secondary="user_rol",
        back_populates="roles"
    )

    # Relación 1:N con Identity (rol contextual)
    identidades = relationship(
        "Identity",
        back_populates="rol"
    )

    def __repr__(self):
        return f"<Role(id={self.id_rol}, nombre={self.nombre})>"
