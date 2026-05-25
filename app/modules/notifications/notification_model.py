# app/modules/notifications/notification_model.py

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id_notification = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type = Column(String(50), nullable=False, index=True)

    title = Column(String(150), nullable=False)

    message = Column(Text, nullable=False)

    entity_type = Column(String(50), nullable=True)
    entity_id = Column(Integer, nullable=True)

    url = Column(String(255), nullable=True)

    is_read = Column(Boolean, default=False, nullable=False, index=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    read_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="notifications")
