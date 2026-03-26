"""Tests for constants enum values."""

from app.constants import UserRole, OrderStatus, PaymentStatus


def test_user_role_values():
    """UserRole enum should expose expected role strings."""
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.RESTAURANT.value == "restaurant"
    assert UserRole.REGULAR_USER.value == "regular_user"


def test_order_status_values():
    """OrderStatus enum should expose expected status strings."""
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.ACCEPTED.value == "accepted"
    assert OrderStatus.PREPARING.value == "preparing"
    assert OrderStatus.ASSIGNED.value == "assigned"
    assert OrderStatus.CANCELLED.value == "cancelled"
    assert OrderStatus.DECLINED.value == "declined"


def test_payment_status_values():
    """PaymentStatus enum should expose expected payment strings."""
    assert PaymentStatus.UNPAID.value == "pending"
    assert PaymentStatus.ACCEPTED.value == "accepted"
    assert PaymentStatus.REJECTED.value == "rejected"
