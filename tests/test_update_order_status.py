"""
Tests for updating order status
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def test_update_order_status():
    """
    Test updating order status and customer notification logic.
    """
    order = database.create_order(
        user_id=123,
        restaurant_id=1,
        items=["Pizza"]
    )
    order_id = order["orderId"]
    response = client.patch(f"/orders/{order_id}/status", json={"new_status": "preparing"})
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == "preparing"
    assert updated_order["customerNotified"] is True
    assert len(updated_order["notifications"]) == 1
    response = client.patch(f"/orders/{order_id}/status", json={"new_status": "ready for pickup"})
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == "ready for pickup"
    assert updated_order["customerNotified"] is True
    assert len(updated_order["notifications"]) == 2
    response = client.patch(f"/orders/{order_id}/status", json={"new_status": "ready for pickup"})
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == "ready for pickup"
    assert updated_order["customerNotified"] is False
def test_update_order_status_nonexistent_order():
    """
    Test updating status of a non-existent order.
    """
    response = client.patch("/orders/9999/status", json={"new_status": "preparing"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
def test_update_order_status_invalid_status():
    """
    Test updating order status with an invalid status value.
    """
    order = database.create_order(
        user_id=456,
        restaurant_id=1,
        items=["Burger"]
    )
    order_id = order["orderId"]
    response = client.patch(f"/orders/{order_id}/status", json={"new_status": ""})
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == ""
    assert updated_order["customerNotified"] is True

