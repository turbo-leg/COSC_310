"""
Handles order-related operations.
"""

from typing import List
from datetime import datetime, timedelta
from fastapi import HTTPException
from app import database, schemas
from app.services.delivery_service import calculate_delivery_cost
from app.constants import OrderStatus, PaymentStatus

def _build_tracking_response(order: dict) -> dict:
    """
    Builds a consistent tracking response for an order.
    """
    created_at_str = order.get("createdAt")
    estimated_delivery_minutes = order.get("estimatedDeliveryMinutes", 0)

    if not created_at_str:
        raise ValueError("Order is missing createdAt")

    created_at = datetime.fromisoformat(created_at_str)
    estimated_arrival = created_at + timedelta(minutes=estimated_delivery_minutes)
    now = datetime.now()

    minutes_remaining = max(
        0,
        int((estimated_arrival - now).total_seconds() // 60)
    )

    return {
        "orderId": order.get("orderId"),
        "status": order.get("status"),
        "createdAt": created_at_str,
        "estimatedDeliveryMinutes": estimated_delivery_minutes,
        "estimatedArrivalTime": estimated_arrival.isoformat(),
        "minutesRemaining": minutes_remaining,
    }

class OrderService:
    """
    Handles order retrieval logic, like fetching orders for a restaurant.
    """
    def place_order(self, request: schemas.OrderCreateRequest):
        """
        Places a new order in the system, with delivery fee logic.
        """
        delivery_fee = calculate_delivery_cost(
            request.distance_km, request.time_minutes
            )
        
        return database.create_order(
            user_id=request.user_id,
            restaurant_id=request.restaurant_id,
            items=request.items,
            time_minutes=request.time_minutes,
            delivery_fee = delivery_fee
        )

    def get_orders_by_restaurant(self, restaurant_id: int):
        """
        Returns all incoming orders for a given restaurant.
        """
        return database.get_incoming_orders_for_restaurant(restaurant_id)

    def get_orders_by_user(self, user_id: int):
        """
        Returns all orders placed by a specific user.
        """
        return database.get_orders_for_user(user_id)

    def update_payment(self, order_id: int, status: str):
        """
        Updates payment status of an order.
        """
        status_value = status.value if isinstance(status, PaymentStatus) else str(status).lower()
        blocked_statuses = [PaymentStatus.REJECTED.value, OrderStatus.DECLINED.value]
        if status_value in blocked_statuses:
            raise HTTPException(
                status_code=400,
                detail="Payment declined. Cannot process transaction."
            )
        updated_order = database.update_payment_status(order_id, status_value)
        if not updated_order:
            raise HTTPException(
                status_code=404,
                detail= "order not Found"
            )
        return updated_order

    def get_restaurant_revenue(self, restaurant_id: int) -> float:
        """
        Returns total correct revenue of restaurant
        """
        return database.get_restaurant_revenue(restaurant_id)

    def track_order(self, order_id: int):
        """
        Returns the status and ETA of a specific order.
        """
        order = database.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return _build_tracking_response(order)

    def track_order_for_restaurant(self, restaurant_id: int) -> List[dict]:
        """
        Returns tracking info for all orders belonging to a restaurant.
        """
        orders = database.get_incoming_orders_for_restaurant(restaurant_id)
        return [_build_tracking_response(order) for order in orders]


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

        allowed_statuses = [OrderStatus.PENDING.value, OrderStatus.ACCEPTED.value]

        if order["status"] not in allowed_statuses:
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

        allowed_statuses = [OrderStatus.PENDING.value, OrderStatus.ACCEPTED.value]
        if order["status"] not in allowed_statuses:
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
    if distance_km < 0:
        raise HTTPException(
            status_code=400,
            detail="Distance cannot be negative")
    for item_id in item_ids:
        item = database.get_menu_item_by_id(item_id)
        if item:
            food_total += item.get("price", 0.0)
    delivery_fee = calculate_delivery_cost(distance_km, time_minutes)
    total_cost = food_total + delivery_fee
    return round(total_cost, 2)
