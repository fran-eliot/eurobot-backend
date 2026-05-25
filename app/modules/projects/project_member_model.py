# app/modules/projects/project_member_model.py

# Este archivo define el modelo de datos para los miembros de un proyecto en la
# aplicación.
# Utiliza SQLAlchemy para definir la estructura de la tabla "project_members" en la
# base de datos, incluyendo sus columnas, tipos de datos, relaciones y restricciones.
# El modelo también incluye un enumerado para los roles de los miembros dentro del
# proyecto, como "coordinator" y "member". Este modelo establece las relaciones
# necesarias con los modelos de proyecto y usuario para facilitar la gestión de los
# miembros dentro de cada proyecto.


import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProjectRoleEnum(enum.StrEnum):
    coordinator = "coordinator"
    member = "member"


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id_project"), nullable=False)

    user_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    role = Column(Enum(ProjectRoleEnum), nullable=False)

    project = relationship("Project", back_populates="members")
    user = relationship("User")
