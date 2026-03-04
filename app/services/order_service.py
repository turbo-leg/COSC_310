"""
Handles order-related operations.
"""

from app.models import Order

class OrderService:
    """
    Handles order retrieval logic, like fetching orders for a restaurant.
    """

    def get_orders_by_restaurant(self, restaurant_id: int):
        """
        Returns all orders for a given restaurant.
        """
        return [
            order for order in Order.orders
            if order.restaurant_id == restaurant_id
        ]

order_service = OrderService()
