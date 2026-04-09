"""Tests for promo codes."""
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app import database

client = TestClient(app)


def setup_data():
    """
    Dummy data
    """
    database.promo_codes_map.clear()
    database.orders_map.clear()
    database.menu_items.clear()

    database.menu_items.append({
        "itemId": 1,
        "restaurantId": 1,
        "name": "Burger",
        "description": "Test",
        "price": 20.0,
        "isActive": True
    })


def create_promo(code="SAVE10", discount=10, days=1, users=None):
    """
    Creates dummy promo code
    """
    expiry = (datetime.now() + timedelta(days=days)).isoformat()
    database.create_promo_code(code, discount, expiry, users)


def test_valid_promo():
    """
    Tests with valid promo code
    """
    setup_data()
    create_promo()

    response = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "SAVE10",
        "user_id": 1
    })

    assert response.status_code == 200
    assert response.json()["total_order_cost"] >= 0


def test_invalid_promo():
    """
    Tests with invalid promo code
    """
    setup_data()

    response = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "BAD",
        "user_id": 1
    })

    assert response.status_code == 400


def test_expired_promo():
    """
    Tests with expired promo code
    """
    setup_data()
    create_promo(days=-1)

    response = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "SAVE10",
        "user_id": 1
    })

    assert response.status_code == 400


def test_wrong_user():
    """
    Tests promo codes being assigned to specific users
    """
    setup_data()
    create_promo(users=[2])

    response = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "SAVE10",
        "user_id": 1
    })

    assert response.status_code == 403


def test_reuse_promo():
    """
    Tests with same promo code used by same user more than once
    """
    setup_data()
    create_promo()

    first = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "SAVE10",
        "user_id": 1
    })

    second = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "SAVE10",
        "user_id": 1
    })

    assert first.status_code == 200
    assert second.status_code == 400


def test_global_promo():
    """
    Tests with promo code that any user can apply towards total cost
    """
    setup_data()
    create_promo(users=None)

    response = client.post("/orders/calculate-total-cost", json={
        "item_ids": [1],
        "distance_km": 5,
        "time_minutes": 20,
        "promo_code": "SAVE10",
        "user_id": 99
    })

    assert response.status_code == 200
