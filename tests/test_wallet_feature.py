"""Tests for customer wallet preload and wallet-backed payments."""

from fastapi.testclient import TestClient

from app import database
from app.main import app
from app.token import create_token

client = TestClient(app)


def _auth_header(user: dict) -> dict:
    """Build auth header for a test user."""
    token = create_token(user)
    return {"Authorization": f"Bearer {token}"}


def setup_function():
    """Reset in-memory storage before each test."""
    database.users_map = {
        1: {
            "userId": 1,
            "name": "Customer One",
            "email": "customer1@test.com",
            "password": "hashed",
            "role": "customer",
            "walletBalance": 0.0,
        },
        2: {
            "userId": 2,
            "name": "Restaurant One",
            "email": "restaurant@test.com",
            "password": "hashed",
            "role": "restaurant",
            "walletBalance": 0.0,
        },
    }
    database.menu_items = [
        {
            "itemId": 10,
            "restaurantId": 2,
            "name": "Burger",
            "description": "Burger",
            "price": 12.0,
            "isActive": True,
        }
    ]
    database.orders_map = {}
    database.NEXT_ORDER_ID = 1


def test_wallet_top_up_adds_money():
    """Customer can add funds to their own wallet."""
    user = database.users_map[1]

    response = client.post(
        "/wallet/top-up",
        json={"amount": 25.5},
        headers=_auth_header(user),
    )

    assert response.status_code == 200
    assert response.json()["walletBalance"] == 25.5
    assert database.users_map[1]["walletBalance"] == 25.5


def test_wallet_balance_does_not_change_without_topup_or_spend():
    """Wallet balance stays stable unless topped up or spent."""
    user = database.users_map[1]
    database.users_map[1]["walletBalance"] = 30.0

    response = client.get("/wallet/me", headers=_auth_header(user))

    assert response.status_code == 200
    assert response.json()["walletBalance"] == 30.0
    assert database.users_map[1]["walletBalance"] == 30.0


def test_restaurant_cannot_use_wallet_endpoint():
    """Non-customers cannot use customer wallet endpoints."""
    restaurant = database.users_map[2]

    response = client.post(
        "/wallet/top-up",
        json={"amount": 10.0},
        headers=_auth_header(restaurant),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only customers can use wallet endpoints"


def test_full_wallet_payment_without_card():
    """Wallet can fully pay for an order."""
    customer = database.users_map[1]
    database.users_map[1]["walletBalance"] = 50.0

    order = database.create_order(
        user_id=1,
        restaurant_id=2,
        items=[10],
        time_minutes=10,
        delivery_fee=5.0,
    )

    response = client.post(
        "/payments/process",
        json={"order_id": order["orderId"]},
        headers=_auth_header(customer),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Payment accepted!"
    assert data["wallet_applied"] == 17.0
    assert data["card_charged"] == 0.0
    assert data["amount_due"] == 0.0
    assert database.orders_map[order["orderId"]]["payment_status"] == "accepted"
    assert database.users_map[1]["walletBalance"] == 33.0


def test_partial_wallet_payment_requests_remaining_amount():
    """If wallet is short, the order becomes partially paid and remaining amount is returned."""
    customer = database.users_map[1]
    database.users_map[1]["walletBalance"] = 5.0

    order = database.create_order(
        user_id=1,
        restaurant_id=2,
        items=[10],
        time_minutes=10,
        delivery_fee=5.0,
    )

    response = client.post(
        "/payments/process",
        json={"order_id": order["orderId"]},
        headers=_auth_header(customer),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Partial wallet payment applied. Additional payment required."
    assert data["wallet_applied"] == 5.0
    assert data["card_charged"] == 0.0
    assert data["amount_due"] == 12.0
    assert database.orders_map[order["orderId"]]["payment_status"] == "partial"
    assert database.users_map[1]["walletBalance"] == 0.0


def test_customer_cannot_pay_someone_elses_order():
    """Authenticated user cannot trigger payment for another customer's order."""
    database.users_map[3] = {
        "userId": 3,
        "name": "Customer Two",
        "email": "customer2@test.com",
        "password": "hashed",
        "role": "customer",
        "walletBalance": 100.0,
    }

    order = database.create_order(
        user_id=1,
        restaurant_id=2,
        items=[10],
        time_minutes=10,
        delivery_fee=5.0,
    )

    response = client.post(
        "/payments/process",
        json={
            "order_id": order["orderId"],
            "credit_card": "1234567812345678",
        },
        headers=_auth_header(database.users_map[3]),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can only pay for your own orders."