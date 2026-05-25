# app/modules/projects/task_model.py

# Este archivo define el modelo de datos para las tareas en la aplicación.
# Utiliza SQLAlchemy para definir la estructura de la tabla "tasks" en la base
# de datos, incluyendo sus columnas, tipos de datos, relaciones y restricciones.
# El modelo también incluye un método de representación para facilitar la depuración
# y visualización de los objetos de tarea.


import enum
from datetime import UTC, datetime

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class TaskStatusEnum(enum.StrEnum):
    todo = "todo"
    doing = "doing"
    done = "done"


class TaskPriorityEnum(enum.StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    id_task = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer, ForeignKey("projects.id_project", ondelete="CASCADE"), nullable=False
    )

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.todo, nullable=False)

    priority = Column(
        Enum(TaskPriorityEnum), default=TaskPriorityEnum.medium, nullable=False
    )

    assigned_to = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    created_by = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    due_date = Column(Date, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    # Relaciones
    project = relationship("Project", back_populates="tasks")

    assignee = relationship("User", foreign_keys=[assigned_to])

    activities = relationship(
        "Activity", back_populates="task", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Task(id={self.id_task}, name='{self.name}')>"
