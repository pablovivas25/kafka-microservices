from sqlalchemy.orm import Session
from app.domain.models.payment import Payment
from app.domain.models.processed_event import ProcessedEvent
import uuid

class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, order_id: uuid.UUID, amount: float):
        payment = Payment(
            order_id=order_id,
            amount=amount
        )
        self.db.add(payment)
        return payment

    def event_already_processed(self, event_id: uuid.UUID):
        return self.db.query(ProcessedEvent).filter(
            ProcessedEvent.event_id == event_id
        ).first() is not None

    def mark_event_processed(self, event_id: uuid.UUID):
        processed = ProcessedEvent(event_id=event_id)
        self.db.add(processed)

    def get_by_order_id(self, order_id):
       return self.db.query(Payment).filter_by(order_id=order_id).first()

    def get_all_by_order_id(self, order_id):
       return self.db.query(Payment).filter_by(order_id=order_id).all()

