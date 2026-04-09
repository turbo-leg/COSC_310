"""
Endpoints for processing secure order payments.
This connects the frontend payment requests to the backend payment service.
"""
from fastapi import APIRouter, Depends
from app.auth import get_user
from app.schemas import PaymentRequest, PaymentResponse
from app.services.payment_service import process_payment

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/process", response_model=PaymentResponse)
def make_payment(request: PaymentRequest, user: dict = Depends(get_user)):
    """
    Processes a secure payment for an order
    """
    return process_payment(
        order_id=request.order_id,
        payer_user_id=user.get("userId"),
        credit_card=request.credit_card
    )
