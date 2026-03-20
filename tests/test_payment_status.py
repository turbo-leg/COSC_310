"""
Testing for payment accept/reject functionality.
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)


def setup_function():
    """
    Clears orders before each test.
    """
    database.orders_map = {}
    database.NEXT_ORDER_ID = 1


def test_accept_payment():
    """
    Checks if payment can be accepted.
    """
    # create order first
    order = database.create_order(user_id=1, restaurant_id=10, items=[1])

    response = client.patch(f"/orders/{order['orderId']}/payment", json={
        "status": "accepted"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Payment accepted"
    assert response.json()["order"]["payment_status"] == "accepted"


def test_reject_payment():
    """
    Checks if payment can be rejected.
    """
    order = database.create_order(user_id=2, restaurant_id=20, items=[2])

    response = client.patch(f"/orders/{order['orderId']}/payment", json={
        "status": "rejected"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Payment rejected"
    assert response.json()["order"]["payment_status"] == "rejected"


def test_invalid_order_payment():
    """
    Checks if invalid order ID is handled.
    """
    response = client.patch("/orders/999/payment", json={
        "status": "accepted"
    })

    assert response.status_code == 200
    assert response.json()["error"] == "Order not found"


def test_default_payment_pending():
    """
    New orders should have pending payment.
    """
    order = database.create_order(user_id=3, restaurant_id=30, items=[3])

    assert order["payment_status"] == "pending"
