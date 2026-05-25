# app/modules/projects/project_model.py

# Este archivo define el modelo de datos para los proyectos en la aplicación.
# Utiliza SQLAlchemy para definir la estructura de la tabla "projects" en la base
# de datos, incluyendo sus columnas, tipos de datos, relaciones y restricciones.
# El modelo también incluye un método de representación para facilitar la depuración
# y visualización de los objetos de proyecto.

from datetime import UTC, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id_project = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(String(50), default="Activo", nullable=False)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    created_by = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)

    # Relaciones
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    creator = relationship("User", foreign_keys=[created_by])

    members = relationship(
        "ProjectMember", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Project(id={self.id_project}, name='{self.name}')>"
