import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import OrderRepository
from app.infrastructure.kafka_producer import publish_order_created
from app.domain.models.order import Order
from app.application.use_cases.create_order import CreateOrderUseCase
from pydantic import BaseModel

router = APIRouter()

class OrderCreate(BaseModel):
    user_id: uuid.UUID
    amount: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders", status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    use_case = CreateOrderUseCase(db)
    order = use_case.execute(data.user_id, data.amount)

    return {"id": order.id}
