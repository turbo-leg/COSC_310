"""
Endpoints for calculating total order cost.
"""
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.order_service import calculate_total_cost_of_order

router = APIRouter(prefix="/orders", tags=["orders"])

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
