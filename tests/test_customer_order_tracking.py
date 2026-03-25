"""Tests for customer order tracking."""

from datetime import datetime, timedelta
import pytest
from app import database
from fastapi import HTTPException
from app.services.order_service import order_service

@pytest.fixture(autouse=True)
def reset_order_storage():
    """
    Resets the in-memory order storage before each test.
    """
    database.orders_map.clear()
    database.NEXT_ORDER_ID = 1
    yield
    database.orders_map.clear()
    database.NEXT_ORDER_ID = 1

def test_create_order_adds_tracking_fields():
    """
    Tests that creating an order stores status and ETA fields correctly.
    """
    order = database.create_order(user_id=101,
                                  restaurant_id=12,
                                  items=[1, 2, 3],
                                  time_minutes=20)

    assert order["orderId"] == 1
    assert order["userId"] == 101
    assert order["restaurantId"] == 12
    assert order["items"] == [1, 2, 3]
    assert order["status"] == "pending"
    assert "createdAt" in order
    assert "estimatedDeliveryMinutes" in order
    assert "estimatedArrivalTime" in order
    assert order["estimatedDeliveryMinutes"] == 40  # 15 + 5 + 20
    assert not order["notifications"]
    assert order["latestNotification"] is None
    assert order["customerNotified"] is False

def test_get_order_by_id_returns_correct_order():
    """
    Tests that exact order that was created is returned
    """
    created = database.create_order(user_id=101,
                                    restaurant_id=12,
                                    items=[1, 2],
                                    time_minutes=15)
    retrieved = database.get_order_by_id(created["orderId"])

    assert retrieved is not None
    assert retrieved["orderId"] == created["orderId"]
    assert retrieved["userId"] == 101
    assert retrieved["restaurantId"] == 12

def test_get_order_by_id_nonexistent():
    """
    Tests that None is returned when order ID does not exist.
    """
    result = database.get_order_by_id(999)
    assert result is None

def test_update_order_status_changes_status():
    """
    Tests that updating order status changes the status field correctly.
    """
    created = database.create_order(user_id=101,
                                    restaurant_id=12,
                                    items=[1],
                                    time_minutes=10)
    updated = database.update_order_status(created["orderId"], "preparing")

    assert updated is not None
    assert updated["orderId"] == created["orderId"]
    assert updated["status"] == "preparing"
    assert database.orders_map[created["orderId"]]["status"] == "preparing"

def test_update_order_status_nonexistent():
    """
    Tests that None is returned when trying to update status of non-existent order.
    """
    result = database.update_order_status(999, "delivered")
    assert result is None

def test_track_order_returns_status_eta_and_remaining_time():
    """Service should return customer-facing tracking info."""
    created = database.create_order(
        user_id=55,
        restaurant_id=7,
        items=[11, 12],
        time_minutes=20
    )

    # Pretend the order was created 10 minutes ago
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    eta_time = ten_minutes_ago + timedelta(minutes=40)

    created["createdAt"] = ten_minutes_ago.isoformat()
    created["estimatedDeliveryMinutes"] = 40
    created["estimatedArrivalTime"] = eta_time.isoformat()
    created["status"] = "preparing"

    tracked = order_service.track_order(created["orderId"])

    assert tracked is not None
    assert tracked["orderId"] == created["orderId"]
    assert tracked["status"] == "preparing"
    assert tracked["estimatedArrivalTime"] == eta_time.isoformat()

    # 40 total ETA - 10 elapsed = about 30 remaining
    # Allow a tiny range in case the clock moves by a second during the test.
    assert 29 <= tracked["minutesRemaining"] <= 30

def test_track_order_clamps_remaining_time_at_zero():
    """Remaining time should never go below zero."""
    created = database.create_order(
        user_id=90,
        restaurant_id=3,
        items=[1],
        time_minutes=5
    )

    old_time = datetime.now() - timedelta(minutes=200)
    created["createdAt"] = old_time.isoformat()
    created["estimatedDeliveryMinutes"] = 20
    created["estimatedArrivalTime"] = (
        old_time + timedelta(minutes=20)
    ).isoformat()

    tracked = order_service.track_order(created["orderId"])

    assert tracked is not None
    assert tracked["minutesRemaining"] == 0

def test_track_order_raises_404_for_missing_order():
    with pytest.raises(HTTPException) as exc_info:
        order_service.track_order(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Order not found"

def test_status_change_notifies_customer():
    """Customer should be notified when order status changes."""
    created = database.create_order(
        user_id=123,
        restaurant_id=45,
        items=[1, 2],
        time_minutes=15
    )

    updated = database.update_order_status(created["orderId"], "preparing")

    assert updated is not None
    assert updated["status"] == "preparing"
    assert len(updated["notifications"]) == 1
    assert updated["customerNotified"] is True
    assert updated["latestNotification"] is not None
    assert updated["latestNotification"]["oldStatus"] == "pending"
    assert updated["latestNotification"]["newStatus"] == "preparing"

def test_multiple_status_changes_still_notify_customer():
    """Customer should still be notified across multiple real status changes."""
    created = database.create_order(
        user_id=101,
        restaurant_id=12,
        items=[1],
        time_minutes=10
    )

    first = database.update_order_status(created["orderId"], "preparing")
    second = database.update_order_status(created["orderId"], "out-for-delivery")

    assert first["customerNotified"] is True
    assert second["customerNotified"] is True
    assert len(second["notifications"]) == 2
    assert second["notifications"][0]["newStatus"] == "preparing"
    assert second["notifications"][1]["newStatus"] == "out-for-delivery"

def test_status_change_to_same_status_does_not_notify_customer():
    """Customer should not be notified if status is updated to the same value."""
    created = database.create_order(
        user_id=202,
        restaurant_id=34,
        items=[1, 2, 3],
        time_minutes=25
    )

    database.update_order_status(created["orderId"], "preparing")
    updated = database.update_order_status(created["orderId"], "preparing")

    assert updated is not None
    assert updated["status"] == "preparing"
    assert len(updated["notifications"]) == 1
    assert updated["customerNotified"] is False
    assert updated["latestNotification"] is None
