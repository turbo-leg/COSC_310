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
order_service.py
"""
handles the logic for orders/checkout total.
"""
from typing import List
from app.services.delivery_service import calculate_delivery_cost
from app import database

def calculate_total_cost_of_order(item_ids: List[int], distance_km: float, 
                                  time_minutes: int) -> float:
    """
    Calculates the total cost of the order (total food price + delivery fee).
    """
    food_total = 0.0

    for item_id in item_ids:
        item = database.get_menu_item_by_id(item_id)
        if item:
            food_total += item.get("price", 0.0)
    delivery_fee = calculate_delivery_cost(distance_km, time_minutes)
    total_cost = food_total + delivery_fee
    return round(total_cost, 2)
