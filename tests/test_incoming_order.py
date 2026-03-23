# pylint: disable=duplicate-code
"""
Tests for viewing incoming restaurant orders.
"""
from fastapi.testclient import TestClient
from app import database
from app.main import app

client = TestClient(app)


def setup_module(module):  # pylint: disable=unused-argument
    """
    Setup dummy order data for testing.
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
            "food_item": "Fries", "items": [2], 
            "order_time": "12:05", "order_value": 5.0, 
            "status": "pending", "payment_status": "pending"
        },
        3: {
            "order_id": 3, "orderId": 3,
            "restaurant_id": 101, "restaurantId": 101, 
            "customer_id": 3, "userId": 3,
            "food_item": "Pizza", "items": [3], 
            "order_time": "12:10", "order_value": 15.0, 
            "status": "pending", "payment_status": "pending"
        }
    }


def teardown_module(module):  # pylint: disable=unused-argument
    """
    Cleanup dummy order data.
    """
    database.orders_map = {}


def test_view_incoming_orders_success():
    """
    Test retrieval of orders for a restaurant.
    """
    response = client.get("/orders/restaurants/100/orders")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["restaurant_id"] == 100
    assert data[1]["restaurant_id"] == 100


def test_view_incoming_orders_empty():
    """
    Test restaurant with no orders.
    """
    response = client.get("/orders/restaurants/999/orders")

    assert response.status_code == 200
    data = response.json()

    assert data == []
