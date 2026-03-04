"""
This file defines REST API endpoints for viewing restaurant orders.
Controllers receive requests and call services to retrieve data.
"""
from typing import List

from fastapi import APIRouter

from app.schemas import OrderResponse
from app.services.order_service import order_service

router = APIRouter()

@router.get("/restaurants/{restaurant_id}/orders", response_model=List[OrderResponse])
def view_incoming_orders(restaurant_id: int):
    """
    Retrieves all incoming orders for a specific restaurant.
    """
    return order_service.get_orders_by_restaurant(restaurant_id)
