from sqlalchemy.orm import Session
from app.models import Order

class OrderService:
    """
    Handles order retrieval logic, like fetching orders for a restaurant.
    """

    def get_orders_by_restaurant(self, db: Session, restaurant_id: int):
        """
        Returns all orders for a given restaurant.
        """
        return db.query(Order).filter(Order.restaurant_id == restaurant_id).all()

order_service = OrderService()