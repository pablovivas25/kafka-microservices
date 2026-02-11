import uuid
from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric, nullable=False)
    status = Column(String, default="CONFIRMED")
