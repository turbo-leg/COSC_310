"""
This file defines endpoints for delivery cost-related logic.
"""

from fastapi import APIRouter, HTTPException
from app.schemas import DeliveryRequest, DeliveryResponse
from app.services.delivery_service import calculate_delivery_cost

router = APIRouter()


@router.post("/delivery/cost", response_model=DeliveryResponse)
def get_delivery_cost(delivery_request: DeliveryRequest):
    """
    Calculates the delivery cost based on distance and time.
    """
    if delivery_request.distance_km <= 0:
        # Validate distance and time inputs to prevent invalid calculations.
        raise HTTPException(
            status_code=400,
            detail="Invalid delivery address"
        )

    cost = calculate_delivery_cost(
        delivery_request.distance_km,
        delivery_request.time_minutes
    )

    return DeliveryResponse(cost=cost)
