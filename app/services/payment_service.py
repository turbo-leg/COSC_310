"""
Payment service Logic 
"""
import uuid
from fastapi import HTTPException
from app import database

def process_payment(order_id: int, credit_card: str) -> str:
    """
    Handles payment verification.
    """
    if len(credit_card) != 16 or not credit_card.isdigit():
        raise HTTPException(status_code=400, detail="Card is Invalid, must be 16 digits.")

    order = database.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail= "Order Not Found.")

    if order.get("payment_status") == "accepted":
        raise HTTPException(status_code=400, detail="Order Already Paid.")

    database.update_payment_status(order_id, "accepted")

    unique_receipt = uuid.uuid4().hex[:16]

    return f"RCPT_{unique_receipt}"
