"""
This file defines REST API endpoints for viewing restaurant orders.
Controllers receive requests and call services to retrieve data.
"""
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel


from app.schemas import OrderResponse
from app.services.order_service import order_service, calculate_total_cost_of_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/restaurants/{restaurant_id}/orders", response_model=List[OrderResponse])
def view_incoming_orders(restaurant_id: int):
    """
    Retrieves all incoming orders for a specific restaurant.
    """
    return order_service.get_orders_by_restaurant(restaurant_id)

class TotalOrderRequest(BaseModel):
    """
    Schema for total order calculations.
    """
    item_ids: List[int]
    distance_km: float
    time_minutes: int

@router.post("/calculate-total-cost")
def get_total_order_cost(request: TotalOrderRequest):
    """
    returns the total order cost.
    """
    total = calculate_total_cost_of_order(item_ids=request.item_ids,
                                          distance_km=request.distance_km,
                                          time_minutes=request.time_minutes)
    return {"total_order_cost":total}
