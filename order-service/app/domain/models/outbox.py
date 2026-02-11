# app/domain/models/outbox.py

import uuid
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base


class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    published = Column(Boolean, default=False)

