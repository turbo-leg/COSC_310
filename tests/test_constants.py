from app.constants import UserRole, OrderStatus, PaymentStatus


def test_user_role_values():
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.RESTAURANT.value == "restaurant"
    assert UserRole.REGULAR_USER.value == "regular_user"


def test_order_status_values():
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.ACCEPTED.value == "accepted"
    assert OrderStatus.PREPARING.value == "preparing"
    assert OrderStatus.ASSIGNED.value == "assigned"
    assert OrderStatus.CANCELLED.value == "cancelled"
    assert OrderStatus.DECLINED.value == "declined"


def test_payment_status_values():
    assert PaymentStatus.UNPAID.value == "unpaid"
    assert PaymentStatus.ACCEPTED.value == "accepted"
    assert PaymentStatus.REJECTED.value == "rejected"
