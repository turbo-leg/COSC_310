"""
Testing for secure payment processing.
"""
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def setup_function():
    """
    Reset the database state before every test.
    """
    database.orders_map = {
        1: {"orderId": 1, "payment_status": "pending"},
        2: {"orderId": 2, "payment_status": "accepted"}
    }

def test_successful_payment():
    """
    Tests if a valid 16-digit card processes successfully.
    """
    response = client.post("/payments/process", json={
        "order_id": 1,
        "credit_card": "1234567812345678"
    })

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
    response = client.post("/payments/process", json={
        "order_id": 1,
        "credit_card": "12345" 
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Card is Invalid, must be 16 digits."

def test_prevent_double_charge():
    """
    Tests if the system blocks payment for an order that is already paid.
    """
    response = client.post("/payments/process", json={
        "order_id": 2,  
        "credit_card": "1234567812345678"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Order Already Paid."


@patch("app.services.payment_service.uuid.uuid4")
def test_mock_uuid_receipt(mock_uuid):
    """
    Tests that generation of receipts is predictable.
    """
    mock_uuid.return_value.hex = "1234567890abcdef"
    database.orders_map = {
        1:{
            "orderId": 1,
            "payment_status": "pending"
        }
    }

    response = client.post("/payments/process", json={
        "order_id": 1,
        "credit_card": "1234567812345678"
    })

    assert response.status_code == 200
    assert response.json()["transaction_id"] == "RCPT_1234567890abcdef"
