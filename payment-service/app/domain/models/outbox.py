import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base

class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String, nullable=False)
    payload = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
