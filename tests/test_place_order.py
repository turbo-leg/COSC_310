"""
Tests for order placement and related logic.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown dummy data for the tests."""
    database.users_map = {
        100: {"userId": 100, "name": "Restaurant A", "email": "rest@a.com", "role": "restaurant"},
        101: {"userId": 101, "name": "Customer User", "email": "cust@user.com", "role": "customer"}
    }
    database.menu_items = [
        {"itemId": 1, "restaurantId": 100, "name": "Burger", "price": 10.0, "isActive": True}
    ]
    database.orders_map = {}
    database.NEXT_ORDER_ID = 1
    yield
    database.users_map = {}
    database.menu_items = []
    database.orders_map = {}

def test_get_all_restaurants():
    """Test retrieving restaurants derived from menu restaurant ids."""
    response = client.get("/restaurants")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Restaurant 100"
    assert data[0]["userId"] == 100
    assert data[0]["restaurantId"] == 100

def test_place_order_success():
    """Test placing a new order via the POST /orders endpoint."""
    payload = {
        "user_id": 101,
        "restaurant_id": 100,
        "items": [1],
        "time_minutes": 20
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "orderId" in data
    assert data["userId"] == 101
    assert data["restaurantId"] == 100
    assert data["status"] == "pending"

def test_get_user_orders():
    """Test retrieving orders placed by a specific user."""
    database.create_order(user_id=101, restaurant_id=100, items=[1], time_minutes=30)
    response = client.get("/orders/users/101/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["userId"] == 101
    assert data[0]["restaurantId"] == 100
