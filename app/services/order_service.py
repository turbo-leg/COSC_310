"""
Handles order-related operations.
"""

from app import database


class OrderService:
    """
    Handles order retrieval logic, like fetching orders for a restaurant.
    """

    def get_orders_by_restaurant(self, restaurant_id: int):
        """
        Returns all incoming orders for a given restaurant.
        """
        return database.get_incoming_orders_for_restaurant(restaurant_id)


order_service = OrderService()
