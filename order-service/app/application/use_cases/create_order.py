import json
from app.domain.models.order import Order
from app.domain.models.outbox import Outbox


class CreateOrderUseCase:

    def __init__(self, db):
        self.db = db

    def execute(self, user_id: str, amount: float):

        order = Order(
            user_id=user_id,
            amount=amount
        )

        self.db.add(order)
        self.db.flush()  # Para obtener order.id antes del commit

        event = Outbox(
            event_type="OrderCreated",
            payload=json.dumps({
                "order_id": str(order.id),
                "user_id": str(order.user_id),
                "amount": float(order.amount)
            })
        )

        self.db.add(event)

        self.db.commit()
        self.db.refresh(order)

        return order
