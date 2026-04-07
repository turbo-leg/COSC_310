"""
Payment service logic.
"""
import uuid
from fastapi import HTTPException
from app import database
from app.constants import PaymentStatus

def _validate_credit_card(credit_card: str | None) -> str | None:
    """
    Logic for checking if credit card is valid.
    """
    if credit_card is None or credit_card == "":
        return None

    if len(credit_card) != 16 or not credit_card.isdigit():
        raise HTTPException(status_code=400, detail="Card is Invalid, must be 16 digits.")

    return credit_card

def _round_money(value: float) -> float:
    """
    Rounds a monetary value to 2 decimal places.
    """
    return round(float(value), 2)

def process_payment(order_id: int, payer_user_id: int, credit_card: str | None = None) -> dict:
    """
    Apply wallet funds first, then charge remaining amount to credit card.
    Returns a receipt with transaction details.
    """
    card = _validate_credit_card(credit_card)

    order = database.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail= "Order Not Found.")

    if order.get("userId") != payer_user_id:
        raise HTTPException(status_code=403, detail="You can only pay for your own orders.")

    if order.get("payment_status") == PaymentStatus.ACCEPTED.value:
        raise HTTPException(status_code=400, detail="Order Already Paid.")

    user = database.get_user_by_id(payer_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User.")

    remaining_due = _round_money(
        order.get("amount_due", order.get("total_cost", order.get("order_value", 0.0)))
    )

    wallet_balance = _round_money(user.get("walletBalance", 0.0))
    wallet_applied = min(wallet_balance, remaining_due)
    if wallet_applied > 0:
        database.deduct_wallet_funds(payer_user_id, wallet_applied)
        order["wallet_applied"] = _round_money(order.get("wallet_applied", 0.0) + wallet_applied)
        order["amount_paid"] = _round_money(order.get("amount_paid", 0.0) + wallet_applied)
        remaining_due = _round_money(remaining_due - wallet_applied)
        order["amount_due"] = remaining_due

    updated_user = database.get_user_by_id(payer_user_id)
    remaining_wallet_balance = _round_money(updated_user.get("walletBalance", 0.0))

    if remaining_due > 0 and not card:
        database.update_payment_status(order_id, PaymentStatus.PARTIAL.value)
        return {
            "transaction_id": "",
            "message": "Partial wallet payment applied. Additional payment required.",
            "wallet_applied": wallet_applied,
            "card_charged": 0.0,
            "remaining_wallet_balance": remaining_wallet_balance,
            "amount_due": remaining_due,
        }

    card_charged = 0.0
    transaction_id = ""

    if remaining_due > 0 and card:
        card_charged = remaining_due
        order["amount_paid"] = _round_money(order.get("amount_paid", 0.0) + card_charged)
        order["amount_due"] = 0.0
        transaction_id = f"RCPT_{uuid.uuid4().hex[:16]}"

    database.update_payment_status(order_id, PaymentStatus.ACCEPTED.value)

    if not transaction_id:
        transaction_id = f"WALLET_{uuid.uuid4().hex[:12]}"

    return {
        "transaction_id": transaction_id,
        "message": "Payment accepted!",
        "wallet_applied": wallet_applied,
        "card_charged": card_charged,
        "remaining_wallet_balance": remaining_wallet_balance,
        "amount_due": 0.0,
    }
