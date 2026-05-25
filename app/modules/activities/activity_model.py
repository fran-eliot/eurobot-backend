# app/modules/activitities/activity_model.py

# Este archivo define el modelo de datos para las actividades en la aplicación.
# Utiliza SQLAlchemy para definir la estructura de la tabla "activities" en la base
# de datos, incluyendo sus columnas, tipos de datos, relaciones y restricciones.
# El modelo también incluye un método de representación para facilitar la depuración
# y visualización de los objetos de actividad.


from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id_activity = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    description = Column(Text, nullable=True)

    status = Column(String(30), nullable=False, default="Pendiente")

    task_id = Column(
        Integer, ForeignKey("tasks.id_task", ondelete="CASCADE"), nullable=False
    )

    user_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    time_spent = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)

    # Relaciones
    task = relationship("Task", back_populates="activities")

    # Usuario que realizó la actividad
    user = relationship("User", back_populates="activities")

    # Adjuntos asociados a la actividad
    attachments = relationship(
        "ActivityAttachment",
        back_populates="activity",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return (
            f"<Activity(id={self.id_activity}, name={self.name},"
            f" hours={self.time_spent})>"
        )
