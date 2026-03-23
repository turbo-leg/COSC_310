"""
Tests for updating order status.
"""
# pylint: disable=duplicate-code

from fastapi.testclient import TestClient
from app.main import app
from app import database
from app.schemas import UpdateOrderStatusRequest

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
        }
    }
def test_update_order_status_success():
    """
    Test successful update of order status.
    """
    request_data = UpdateOrderStatusRequest(new_status="preparing")
    response = client.patch("/orders/1/status", json=request_data.dict())

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == 1
    assert data["status"] == "preparing"

def test_update_order_status_not_found():
    """
    Test updating status of a order that does not exist.
    """
    request_data = UpdateOrderStatusRequest(new_status="preparing")
    response = client.patch("/orders/999/status", json=request_data.dict())

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order not found"
def test_update_order_status_invalid_status():
    """
    Test updating status with an invalid status value.
    """
    request_data = {"new_status": "invalid_status"}
    response = client.patch("/orders/1/status", json=request_data)

    assert response.status_code == 422  # Unprocessable Entity for validation error

