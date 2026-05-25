# app/modules/activity_feed/activity_feed_model.py
# 📋 Modelo de actividad de proyecto: representa las actividades relacionadas con un
# proyecto específico, incluyendo acciones como creación de tareas, cambios de estado,
# comentarios, etc. Este modelo se utiliza para registrar y mostrar el historial de
# actividades dentro de un proyecto, proporcionando contexto y trazabilidad para los
# usuarios. Incluye información sobre el tipo de actividad, el usuario que la realizó,
# la entidad afectada y un mensaje descriptivo de la actividad.

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProjectActivityFeed(Base):
    __tablename__ = "project_activity_feed"

    id_feed = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id_project", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    event_type = Column(String(50), nullable=False, index=True)
    message = Column(String(255), nullable=False)

    entity_type = Column(String(50), nullable=True)
    entity_id = Column(Integer, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    project = relationship("Project")
    user = relationship("User")
