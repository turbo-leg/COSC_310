# pylint: disable=duplicate-code
"""
Tests for modifying and cancelling orders.
"""
from fastapi.testclient import TestClient
from app import database
from app.main import app

client = TestClient(app)

def setup_function(function):  # pylint: disable=unused-argument
    """
    Setup dummy order data for testing modifications as a dictionary.
    """
    database.orders_map = {
        1: {
            "order_id": 1, "orderId": 1,
            "restaurant_id": 100, "restaurantId": 100, 
            "customer_id": 1, "userId": 1,
            "food_item": "Burger", "items": [1], 
            "order_time": "12:00", "order_value": 10.0, 
            "status": "pending", "payment_status": "pending"
        },
        2: {
            "order_id": 2, "orderId": 2,
            "restaurant_id": 100, "restaurantId": 100, 
            "customer_id": 2, "userId": 2,
            "food_item": "Pizza", "items": [3], 
            "order_time": "12:10", "order_value": 15.0, 
            "status": "preparing", "payment_status": "accepted"
        }
    }

def teardown_function(function):  # pylint: disable=unused-argument
    """
    Cleanup dummy order data to an empty dictionary.
    """
    database.orders_map = {}

def test_cancel_order_success():
    """Test cancelling an order that is still pending."""

    response = client.put("/orders/1/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

def test_cancel_order_too_late():
    """Test cancelling an order that is already being prepared."""

    response = client.put("/orders/2/cancel")
    assert response.status_code == 400
    assert "Cannot cancel order" in response.json()["detail"]

def test_modify_order_success():
    """Test modifying an order that is still pending."""

    payload = {"food_item": "Curly Fries", "order_value": 12.0}
    response = client.put("/orders/1/modify", json=payload)

    assert response.status_code == 200
    assert response.json()["food_item"] == "Curly Fries"
    assert response.json()["order_value"] == 12.0

def test_modify_order_too_late():
    """Test modifying an order that is already being prepared."""

    payload = {"food_item": "Salad"}
    response = client.put("/orders/2/modify", json=payload)

    assert response.status_code == 400
    assert "Cannot modify order" in response.json()["detail"]

def test_action_on_missing_order():
    """Test attempting to modify an order that doesn't exist."""

    response = client.put("/orders/999/cancel")
    assert response.status_code == 404
