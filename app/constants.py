"""
This module defines constants and enumerations used throughout the application."""

from enum import Enum


class UserRole(str, Enum):
    """Supported user roles."""
    ADMIN = "admin"
    RESTAURANT = "restaurant"
    REGULAR_USER = "regular_user"
    CUSTOMER = "customer"


class OrderStatus(str, Enum):
    """Supported order lifecycle statuses."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    ASSIGNED = "assigned"
    OUT_FOR_DELIVERY = "out-for-delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    DECLINED = "declined"


class PaymentStatus(str, Enum):
    """Supported payment states."""
    UNPAID = "pending"
    PARTIAL = "partial"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class NotificationType(str, Enum):
    """Supported notification event types."""
    ORDER_CREATED = "order_created"
    ORDER_UPDATED = "order_updated"
    PAYMENT_ACCEPTED = "payment_accepted"
    PAYMENT_REJECTED = "payment_rejected"
    DELIVERY_ASSIGNED = "delivery_assigned"
    ORDER_CANCELLED = "order_cancelled"


class RefundStatus(str, Enum):
    """Supported refund request states."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"


class RefundReason(str, Enum):
    """Supported reasons for requesting a refund."""
    NEVER_ARRIVED = "never_arrived"
    WRONG_ORDER = "wrong_order"
    POOR_QUALITY = "poor_quality"
    MISSING_ITEMS = "missing_items"
    OTHER = "other"
