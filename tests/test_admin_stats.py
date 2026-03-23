"""
Tests for admin endpoints.
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def test_admin_stats_access():
    """
    Test that an admin gets stats and regular user is forbidden.
    """
    database.users_map.clear()
    database.orders_map.clear()
    database.menu_items.clear()
    admin_user = database.create_user("Admin", "admin@email.com", "password123", "admin")
    regular_user = database.create_user("User", "user@email.com", "password123", "Regular User")
    response = client.get(f"/admin/stats?user_id={regular_user['userId']}")
    assert response.status_code == 403
    response = client.get(f"/admin/stats?user_id={admin_user['userId']}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] == 2
    assert data["total_orders"] == 0
    assert data["total_revenue"] == 0.0
    assert data["total_menu_items"] == 0

def test_admin_stats_data():
    """
    Test stats calculation logic.
    """
    database.users_map.clear()
    database.orders_map.clear()
    database.menu_items.clear()
    admin_user = database.create_user("Admin", "admin@email.com", "password123", "admin")
    _ = database.create_user("User", "user@email.com", "password123", "Regular User")
    item1 = database.create_menu_item(1, "Burger", "Good", 10.5)
    item2 = database.create_menu_item(1, "Fries", "Good", 5.0)
    _ = database.create_order(1, 1, [item1["itemId"], item2["itemId"]], 15)
    _ = database.create_order(2, 1, [item1["itemId"]], 10)
    response = client.get(f"/admin/stats?user_id={admin_user['userId']}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] == 2
    assert data["total_orders"] == 2
    assert data["total_revenue"] == 26.0  # 10.5 + 5.0 + 10.5
    assert data["total_menu_items"] == 2
