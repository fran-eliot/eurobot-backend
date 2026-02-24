# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class User(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    identidades = relationship(
        "Identity",
        back_populates="usuario",
        cascade="all, delete"
    )

    roles = relationship(
        "Role",
        secondary="user_rol",
        back_populates="usuarios"
    )

    def __repr__(self):
        return f"<User(id={self.id_usuario}, nombre={self.nombre})>"
