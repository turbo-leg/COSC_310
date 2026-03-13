"""Tests to ensure customers are notified when the order status changes"""

from app import database

def test_notify_customer_valid():
    """ Test case to validate that notify_customer returns 
    the correct order status for a valid user. """
    database.users_map = {
        1: {"userId": 1, "name": "Alice", "email": "alice@example.com"}
    }
    database.orders_map = {
        1: {"orderId": 1, "userId": 1, "restaurantId": 1, "items": [], "status": "pending"}
    }

    result = database.notify_customer(1)
    assert result == "Your order status is now: pending"

def test_notify_customer_invalid_user():
    """ Test case to validate that notify_customer returns None for an invalid user. """
    database.users_map = {}
    database.orders_map = {}

    result = database.notify_customer(999)
    assert result is None
