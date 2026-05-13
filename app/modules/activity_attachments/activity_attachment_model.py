# app/modules/activity_attachments/activity_attachment_model.py

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class ActivityAttachment(Base):
    __tablename__ = "activity_attachments"

    id_attachment = Column(Integer, primary_key=True, index=True)

    activity_id = Column(
        Integer,
        ForeignKey("activities.id_activity", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
        index=True,
    )

    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(150), nullable=True)
    size_bytes = Column(Integer, nullable=False, default=0)

    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    activity = relationship(
        "Activity",
        back_populates="attachments",
    )

    uploader = relationship(
        "User",
        back_populates="activity_attachments",
    )

    def __repr__(self):
        return (
            f"<ActivityAttachment("
            f"id={self.id_attachment}, "
            f"filename={self.original_filename})>"
        )