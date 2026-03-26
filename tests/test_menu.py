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
    database.users_map = {
        100: {
            "userId": 100, "name": "Rest O", "email": "a@b.com",
            "password": "pass", "role": "restaurant"
        },
        102: {
            "userId": 102, "name": "Fake", "email": "f@b.com",
            "password": "pass", "role": "customer"
        }
    }
    database.menu_items = [
        {
            "itemId": 1,
            "restaurantId": 100,
            "name": "Burger",
            "description": "Big Mac",
            "price": 10.0,
            "isActive": True
        }
    ]

def teardown_module(module): # pylint: disable=unused-argument
    """
    Cleanup dummy data.
    """
    database.menu_items = []
    database.users_map = {}

def test_get_restaurant_menu_success():
    """
    Test retrieval of menu items for a restaurant.
    """
    response = client.get("/restaurant/100/menu")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Burger"
    assert data[0]["isActive"] is True

def test_get_restaurant_menu_not_found():
    """
    Test 404 when restaurant does't exist.
    """
    response = client.get("/restaurant/999/menu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"

def test_add_menu_item_success():
    """
    Test adding a new menu item successfully.
    """
    payload = {
        "name": "Fries",
        "description": "Mcdonalds",
        "price": 4.5
    }
    response = client.post("/restaurant/100/menu?owner_id=100", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Fries"
    assert data["price"] == 4.5
    assert data["isActive"] is True

def test_add_menu_item_unauthorized():
    """
    Test adding a new menu item with unauthorized user.
    """
    payload = {"name": "Fries", "description": "Mcdonalds", "price": 4.5}
    response = client.post("/restaurant/100/menu?owner_id=102", json=payload)
    assert response.status_code == 403

def test_edit_menu_item_success():
    """
    Test editing a menu item.
    """
    payload = {"price": 12.0}
    response = client.put("/restaurant/100/menu/1?owner_id=100", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 12.0

def test_edit_menu_item_not_found():
    """
    Test editing a non-existent item.
    """
    response = client.put("/restaurant/100/menu/99?owner_id=100", json={"price": 12.0})
    assert response.status_code == 404

def test_remove_menu_item_success():
    """
    Test removing an item.
    """
    response = client.delete("/restaurant/100/menu/1?owner_id=100")
    assert response.status_code == 200
    resp = client.get("/restaurant/100/menu")
    assert resp.status_code in [200, 404]

def test_get_restaurants_with_search():
    """ Test searching for a restaurant by name. """
    database.users_map = {
        100: {"userId": 100, "name": "Pizza", "role": "restaurant",
             "email": "pizza@gmail.com", "password": "password123"},
        101: {"userId": 101, "name": "Burger", "role": "restaurant",
             "email": "burger@gmail.com", "password": "password123"},
    }
    response = client.get("/restaurants?query=pizza")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Pizza"

def test_get_restaurants_without_search():
    """ Test getting all restaurants. """
    database.users_map = {
        100: {"userId": 100, "name": "Pizza", "role": "restaurant",
             "email": "pizza@gmail.com", "password": "password123"},
        101: {"userId": 101, "name": "Burger", "role": "restaurant",
             "email": "burger@gmail.com", "password": "password123"},
    }
    response = client.get("/restaurants")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
