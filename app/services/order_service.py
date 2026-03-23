"""
Handles order-related operations.
"""
from fastapi import HTTPException

from typing import List
from datetime import datetime
from app import database, schemas
from app.services.delivery_service import calculate_delivery_cost

class OrderService:
    """
    Handles order retrieval logic, like fetching orders for a restaurant.
    """

    def get_orders_by_restaurant(self, restaurant_id: int):
        """
        Returns all incoming orders for a given restaurant.
        """
        return database.get_incoming_orders_for_restaurant(restaurant_id)
    def update_payment(self, order_id: int, status: str):
        """
        Updates payment status of an order.
        """
        return database.update_payment_status(order_id, status)

    def track_order(self, order_id: int):
        """
        Returns the status and ETA of a specific order.
        """
        order = database.get_order_by_id(order_id)
        if not order:
            return None

        created_at = datetime.fromisoformat(order["createdAt"])
        eta_minutes = order["estimatedDeliveryMinutes"]
        estimated_arrival = datetime.fromisoformat(order["estimatedArrivalTime"])

        elapsed_time = (datetime.now() - created_at).total_seconds() // 60
        minutes_remaining = max(0, eta_minutes - elapsed_time)

        return {
            "orderId": order["orderId"],
            "status": order["status"],
            "estimatedArrivalTime": estimated_arrival.isoformat(),
            "minutesRemaining": minutes_remaining
        }

    def update_order_status(self, order_id: int, new_status: str):
        """
        Updates the status of an order (e.g., from 'pending' to 'preparing').
        """
        return database.update_order_status(order_id, new_status)
    def cancel_order(self, order_id: int):
        """
        Cancels Order.
        """
        order = database.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code = 404, detail="Order Not Found")

        if order["status"] not in ["pending", "accepted"]:
            raise HTTPException(
                status_code=400,
                detail=f"""Cannot cancel order. Current status is {order['status']}""")
        update_order = database.cancel_order_in_database(order_id)
        return update_order


    def modify_order(self, order_id: int, modify_request: schemas.OrderModifyRequest):
        """
        Modifies specific values in the order.
        """
        order = database.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order Not Found")
        if order["status"] not in ["pending", "accepted"]:
            raise HTTPException(
                status_code=400,
                detail=f"""Cannot modify order. Current status is {order['status']}""")
        update_order = database.modify_order_in_database(order_id,
                        modify_request.model_dump(exclude_unset=True))
        return update_order



order_service = OrderService()
"""
handles the logic for orders/checkout total.
"""


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
