from app.domain.models.order import Order

class OrderRepository:

    def __init__(self, db):
        self.db = db

    def add(self, order: Order):
        self.db.add(order)

