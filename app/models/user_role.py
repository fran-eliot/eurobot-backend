# app/models/user_role.py

from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_rol"

    user_id = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        primary_key=True
    )

    rol_id = Column(
        Integer,
        ForeignKey("roles.id_rol", ondelete="CASCADE"),
        primary_key=True
    )
