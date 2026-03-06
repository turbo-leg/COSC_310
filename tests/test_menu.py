"""
Tests for menu controller endpoints.
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
        {
            "itemId": 1,
            "restaurantId": 100,
            "name": "Burger",
            "description": "Big Mac",
            "price": 10.0,
            "isActive": True
        },
        {
            "itemId": 2,
            "restaurantId": 100,
            "name": "Fries",
            "description": "Large fries",
            "price": 5.0,
            "isActive": False
        },
        {
            "itemId": 3,
            "restaurantId": 101,
            "name": "Pizza",
            "description": "Pepperoni pizza",
            "price": 15.0,
            "isActive": True
        }
    ]

def teardown_module(module): # pylint: disable=unused-argument
    """
    Cleanup dummy data.
    """
    database.menu_items = []

def test_get_restaurant_menu_success():
    """
    Test successful retrieval of active menu items for a restaurant.
    """
    response = client.get("/restaurant/100/menu")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Burger"
    assert data[0]["isActive"] is True

def test_get_restaurant_menu_not_found():
    """
    Test 404 when restaurant does not exist.
    """
    response = client.get("/restaurant/999/menu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"
