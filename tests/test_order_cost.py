"""
Tests for order cost calculations.
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def setup_module(module): # pylint: disable=unused-argument
    """
    Setup dummy data for testing.
    """
    database.menu_items = [
        {"itemId": 3, "restaurantId": 1, "name": "Burger", 
         "description": "Good burger", "price": 15.00, "isActive": True},
        {"itemId": 44, "restaurantId": 1, "name": "Fries", 
         "description": "Good fries", "price": 30.00, "isActive": True},
        {"itemId": 81, "restaurantId": 1, "name": "Soda", 
         "description": "Good soda", "price": 36.72, "isActive": True}
    ]

def teardown_module(module): # pylint: disable=unused-argument
    """
    Cleanup dummy data.
    """
    database.menu_items = []

def test_calculate_total_order_cost_correct():
    """
    Testing if total_cost logic is accurate in calculating food prices and delivery.
    """
    valid_data = {
        "item_ids": [3, 44, 81],
        "distance_km": 5.5,
        "time_minutes": 20
    }

    response = client.post("/orders/calculate-total-cost", json=valid_data)

    assert response.status_code == 200
    data = response.json()

    assert "total_order_cost" in data
    assert data["total_order_cost"] == 91.47


def test_calculate_total_order_cost_item_not_found():
    """
    Testing if total_cost logic is accurate when one of the itemIDS does not exist in the database.
    """
    valid_data = {
        "item_ids": [3, 44, 81, 999],
        "distance_km": 5.5,
        "time_minutes": 20
    }

    response = client.post("/orders/calculate-total-cost", json=valid_data)

    assert response.status_code == 200
    data = response.json()

    assert "total_order_cost" in data
    assert data["total_order_cost"] == 91.47
