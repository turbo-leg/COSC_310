"""
Endpoints for processing secure order payments.
This connects the frontend payment requests to the backend payment service.
"""
from fastapi import APIRouter
from app.schemas import PaymentRequest, PaymentResponse
from app.services.payment_service import process_payment

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/process", response_model=PaymentResponse)
def make_payment(request: PaymentRequest):
    """
    Processes a secure payment for an order
    """
    rcpt_id = process_payment(request.order_id, request.credit_card)

    return {
        "transaction_id": rcpt_id, 
        "message": "Payment accepted!"
    }
