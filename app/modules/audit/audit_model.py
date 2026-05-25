# app/modules/audit/audit_log.py

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id_log = Column(Integer, primary_key=True, index=True)

    action = Column(String(100), nullable=False)

    user_id = Column(
        Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True
    )

    resource_type = Column(String(50), nullable=True)

    resource_id = Column(Integer, nullable=True)

    description = Column(String(255))

    ip_address = Column(String(50))

    user_agent = Column(String(255))

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="audit_logs")
