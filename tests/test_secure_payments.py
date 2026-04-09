"""
Testing for secure payment processing.
"""
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app import database
from app.token import create_token

client = TestClient(app)

def _auth_header(user: dict) -> dict:
    """Helper to create auth header for a test user."""
    token = create_token(user)
    return {"Authorization": f"Bearer {token}"}


def setup_function():
    """Reset database state before every test."""
    database.users_map = {
        1: {
            "userId": 1,
            "name": "Customer One",
            "email": "customer1@test.com",
            "password": "hashed",
            "role": "customer",
            "walletBalance": 0.0,
        }
    }
    database.orders_map = {
        1: {
            "orderId": 1,
            "userId": 1,
            "payment_status": "pending",
            "order_value": 20.0,
            "total_cost": 20.0,
            "amount_paid": 0.0,
            "amount_due": 20.0,
            "wallet_applied": 0.0,
        },
        2: {
            "orderId": 2,
            "userId": 1,
            "payment_status": "accepted",
            "order_value": 10.0,
            "total_cost": 10.0,
            "amount_paid": 10.0,
            "amount_due": 0.0,
            "wallet_applied": 0.0,
        },
    }


def test_successful_payment():
    """
    Tests if a valid 16-digit card processes successfully.
    """
    user = database.users_map[1]

    response = client.post("/payments/process", json={
        "order_id": 1,
        "credit_card": "1234567812345678"
    }, headers=_auth_header(user))

    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"].startswith("RCPT_")
    assert len(data["transaction_id"]) > 10
    assert data["message"] == "Payment accepted!"
    assert database.orders_map[1]["payment_status"] == "accepted"

def test_invalid_credit_card_length():
    """
    Tests if the system rejects cards that aren't 16 digits.
    """

    user = database.users_map[1]

    response = client.post("/payments/process", json={
        "order_id": 1,
        "credit_card": "12345"
    }, headers=_auth_header(user))

    assert response.status_code == 400
    assert response.json()["detail"] == "Card is Invalid, must be 16 digits."

def test_prevent_double_charge():
    """
    Tests if the system blocks payment for an order that is already paid.
    """
    user = database.users_map[1]

    response = client.post("/payments/process", json={
        "order_id": 2,
        "credit_card": "1234567812345678"
    }, headers=_auth_header(user))

    assert response.status_code == 400
    assert response.json()["detail"] == "Order Already Paid."


@patch("app.services.payment_service.uuid.uuid4")
def test_mock_uuid_receipt(mock_uuid):
    """
    Tests that generation of receipts is predictable.
    """
    mock_uuid.return_value.hex = "1234567890abcdef"
    user = database.users_map[1]

    response = client.post("/payments/process", json={
        "order_id": 1,
        "credit_card": "1234567812345678"
    }, headers=_auth_header(user))

    assert response.status_code == 200
    assert response.json()["transaction_id"] == "RCPT_1234567890abcdef"
