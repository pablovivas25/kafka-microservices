import uuid
from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric, nullable=False)
    status = Column(String, default="CREATED")
