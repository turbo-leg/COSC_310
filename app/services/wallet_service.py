"""Wallet business logic."""

from fastapi import HTTPException

from app import database
from app.constants import UserRole

CUSTOMER_ROLES = {
    UserRole.CUSTOMER.value,
    UserRole.REGULAR_USER.value,
    "customer",
    "regular_user",
    "Regular User",
}


def _ensure_customer(user: dict) -> dict:
    """Ensure the authenticated user is allowed to use a wallet."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    if user.get("role") not in CUSTOMER_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Only customers can use wallet endpoints",
        )

    return user


def _validate_credit_card(credit_card: str) -> str:
    """Validate the simulated card number used for top-ups."""
    card = (credit_card or "").strip()
    if len(card) != 16 or not card.isdigit():
        raise HTTPException(status_code=400, detail="Card is invalid, must be 16 digits")
    return card


def top_up_wallet(user: dict, amount: float, credit_card: str) -> dict:
    """Add money to the authenticated customer's wallet."""
    customer = _ensure_customer(user)
    _validate_credit_card(credit_card)

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Top-up amount must be positive")

    updated_user = database.add_wallet_funds(customer["userId"], amount)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "userId": updated_user["userId"],
        "walletBalance": round(float(updated_user.get("walletBalance", 0.0)), 2),
    }


def get_wallet_balance(user: dict) -> dict:
    """Get the authenticated customer's wallet balance."""
    customer = _ensure_customer(user)
    return {
        "userId": customer["userId"],
        "walletBalance": round(float(customer.get("walletBalance", 0.0)), 2),
    }
