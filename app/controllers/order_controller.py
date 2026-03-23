"""
This file defines REST API endpoints for viewing restaurant orders.
Controllers receive requests and call services to retrieve data.
"""
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app import schemas


from app.schemas import OrderResponse, TrackOrderResponse, UpdateOrderStatusRequest
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

@router.get("/{order_id}/track", response_model=TrackOrderResponse)
def track_order(order_id: int):
    """
    Returns the status and ETA of a specific order.
    """
    result = order_service.track_order(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, request: UpdateOrderStatusRequest):
    """
    Updates the status of an order (e.g., from 'pending' to 'preparing').
    """
    updated_order = order_service.update_order_status(order_id, request.new_status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order
class PaymentUpdateRequest(BaseModel):
    """
    Schema for updating the payment status.
    """
    status: str  # "accepted" or "rejected"

@router.patch("/{order_id}/payment")
def update_payment_status(order_id: int, request: PaymentUpdateRequest):
    """
    Accepts or rejects payment for an order.
    """
    updated_order = order_service.update_payment(order_id, request.status)

    if not updated_order:
        return {"error": "Order not found"}

    return {
        "message": f"Payment {request.status}",
        "order": updated_order
    }

@router.put("/{order_id}/cancel", response_model=schemas.OrderResponse)
def cancel_order_endpoint(order_id: int):
    """
    Cancels order if preparation hasn't started yet.
    """
    return order_service.cancel_order(order_id)

@router.put("/{order_id}/modify", response_model=schemas.OrderResponse)
def modify_order_endpoint(order_id: int, modify_request: schemas.OrderModifyRequest):
    """
    Modify an order's details/items before preparation starts.
    """
    return order_service.modify_order(order_id, modify_request)
@router.get("/restaurants/{restaurant_id}/track-delivery", response_model=List[TrackOrderResponse])
def track_delivery_for_restaurant(restaurant_id: int):
    """
    Returns delivery tracking info for all orders of a restaurant.
    """
    return order_service.track_order_for_restaurant(restaurant_id)
