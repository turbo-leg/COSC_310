"""
Tests for admin menu toggle endpoint.
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def test_admin_toggle_menu_item_stock():
    """
    Test that an admin can toggle the stock status of a menu item.
    """
    database.users_map.clear()
    database.menu_items.clear()

    admin_user = database.create_user("Admin", "admin@email.com", "password123", "admin")
    regular_user = database.create_user("User", "user@email.com", "password123", "Regular User")

    restaurant_id = 99
    item = database.create_menu_item(restaurant_id, "Test Burger", "A very tasty burger", 15.0)
    item_id = item["itemId"]
    assert item["isActive"] is True
    payload = {"isActive": False}
    response = client.put(
        f"/admin/menu/{item_id}/toggle-stock?user_id={regular_user['userId']}",
        json=payload
    )
    assert response.status_code == 403
    response = client.put(
        f"/admin/menu/{item_id}/toggle-stock?user_id={admin_user['userId']}",
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["isActive"] is False
    db_item = database.get_menu_item_by_id(item_id)
    assert db_item["isActive"] is False
    payload_true = {"isActive": True}
    response = client.put(
        f"/admin/menu/{item_id}/toggle-stock?user_id={admin_user['userId']}",
        json=payload_true
    )
    assert response.status_code == 200
    assert response.json()["isActive"] is True
    db_item = database.get_menu_item_by_id(item_id)
    assert db_item["isActive"] is True

def test_admin_toggle_nonexistent_item():
    """
    Test toggling a non-existent item returns 404.
    """
    database.users_map.clear()
    admin_user = database.create_user("Admin", "admin@email.com", "password123", "admin")

    response = client.put(
        f"/admin/menu/9999/toggle-stock?user_id={admin_user['userId']}",
        json={"isActive": False}
    )
    assert response.status_code == 404
