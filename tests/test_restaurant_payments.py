# pylint: disable=duplicate-code
"""
Tests for restaurant payments and revenue reporting.
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

# pylint: disable=duplicate-code

client = TestClient(app)

def setup_function(function):  # pylint: disable=unused-argument
    """
    Setup mock database before every test.
    """
    database.users_map = {
        100: {"userId": 100, "name": "Burger Joint", "role": "restaurant"},
        101: {"userId": 101, "name": "Pizza Place", "role": "restaurant"},
        102: {"userId": 102, "name": "Customer Steve", "role": "customer"}
    }

    database.orders_map = {
        1: {"orderId": 1, "restaurantId": 100, "order_value": 15.0, "payment_status": "pending"},
        2: {"orderId": 2, "restaurantId": 100, "order_value": 20.5, "payment_status": "accepted"},
        3: {"orderId": 3, "restaurantId": 100, "order_value": 10.0, "payment_status": "accepted"},
        4: {"orderId": 4, "restaurantId": 101, "order_value": 50.0, "payment_status": "accepted"}
    }

def teardown_function(function):  # pylint: disable=unused-argument
    """
    Clear database.
    """
    database.users_map.clear()
    database.orders_map.clear()

def test_payment_success():
    """
    Checks if successfully process a transaction.
    """
    response = client.patch("/orders/1/payment", json={"status": "accepted"})
    assert response.status_code == 200
    assert response.json()["order"]["payment_status"] == "accepted"

def test_payment_declined_error_handling():
    """
    Checks if payment declines, system displays error and prevents processing.
    """
    response = client.patch("/orders/1/payment", json={"status": "declined"})
    assert response.status_code == 400
    assert "Payment declined" in response.json()["detail"]
    assert database.orders_map[1]["payment_status"] == "pending"

def test_get_restaurant_revenue_success():
    """
    Checks if Being able to see the total amount processed.
    Restaurant 100 has one $15 pending order, and two accepted orders ($20.50 + $10.00).
    Total revenue should be $30.50.
    """
    response = client.get("/orders/restaurants/100/revenue?user_id=100")
    assert response.status_code == 200
    assert response.json()["total_revenue"] == 30.5

def test_get_restaurant_revenue_forbidden_wrong_owner():
    """
    Checks if Restaurant 101 cannot view Restaurant 100's revenue.
    """
    response = client.get("/orders/restaurants/100/revenue?user_id=101")
    assert response.status_code == 403

def test_get_restaurant_revenue_forbidden_customer():
    """
    Checks if Customers cannot view revenue.
    """
    response = client.get("/orders/restaurants/100/revenue?user_id=102")
    assert response.status_code == 403
