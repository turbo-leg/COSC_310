"""
Business logic for refund requests.
Handles creation, retrieval, and admin resolution of refunds.
"""
from fastapi import HTTPException
from app import database
from app.constants import OrderStatus, PaymentStatus, RefundStatus


def request_refund(order_id: int, user_id: int, reason: str, description: str) -> dict:
    """
    Creates a refund request for a delivered and paid order.
    Raises 404 if order not found, 403 if user does not own the order,
    400 if order is not eligible for a refund, or 409 if one already exists.
    """
    order = database.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.get("userId") != user_id:
        raise HTTPException(status_code=403, detail="You do not own this order")

    if order.get("status") != OrderStatus.DELIVERED.value:
        raise HTTPException(
            status_code=400,
            detail="Refunds can only be requested for delivered orders"
        )

    if order.get("payment_status") not in (PaymentStatus.ACCEPTED.value, "paid"):
        raise HTTPException(
            status_code=400,
            detail="Refunds can only be requested for paid orders"
        )

    existing = database.get_refund_by_order_id(order_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A refund request already exists for this order"
        )

    return database.create_refund(order_id, user_id, reason, description)


def get_all_refunds() -> list:
    """
    Returns all refund requests (admin only).
    """
    return database.get_all_refunds()


def get_user_refunds(user_id: int) -> list:
    """
    Returns all refund requests for a specific user.
    """
    return database.get_refunds_for_user(user_id)


def handle_refund(refund_id: int, new_status: str) -> dict:
    """
    Approves or denies a refund request.
    Raises 404 if refund not found or 400 if status is invalid.
    """
    if new_status not in (RefundStatus.APPROVED.value, RefundStatus.DENIED.value):
        raise HTTPException(
            status_code=400,
            detail="Status must be 'approved' or 'denied'"
        )

    refund = database.update_refund_status(refund_id, new_status)
    if not refund:
        raise HTTPException(status_code=404, detail="Refund request not found")

    return refund
