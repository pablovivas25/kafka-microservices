from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base
from sqlalchemy.dialects.postgresql import UUID


class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    event_id = Column(UUID(as_uuid=True), primary_key=True)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
