"""
This file defines endpoints for delivery cost-related logic.
"""

from fastapi import APIRouter
from app.schemas import DeliveryRequest, DeliveryResponse
from app.services.delivery_service import calculate_delivery_cost

router = APIRouter()


@router.post("/delivery/cost", response_model=DeliveryResponse)
def get_delivery_cost(request: DeliveryRequest):
    cost = calculate_delivery_cost(
        request.distance_km,
        request.time_minutes
    )

    return DeliveryResponse(cost=cost)
