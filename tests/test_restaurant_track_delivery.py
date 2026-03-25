"""Tests for restaurant delivery tracking."""
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def setup_module(module):  # pylint: disable=unused-argument
    """
    Setup function to reset order storage before each test
    """
    database.orders_map.clear()
    database.NEXT_ORDER_ID = 1

def test_track_delivery_for_restaurant_returns_tracking_info():
    """
    Restaurants should receive tracking info for all their orders.
    """
    now = datetime.now()

    database.orders_map = {
        1: {
            "orderId": 1,
            "restaurantId": 100,
            "userId": 1,
            "items": [1],
            "status": "preparing",
            "createdAt": (now - timedelta(minutes=10)).isoformat(),
            "estimatedDeliveryMinutes": 40,
            "estimatedArrivalTime": (now + timedelta(minutes=30)).isoformat(),
            "payment_status": "pending",
        },
        2: {
            "orderId": 2,
            "restaurantId": 100,
            "userId": 2,
            "items": [2],
            "status": "out-for-delivery",
            "createdAt": (now - timedelta(minutes=20)).isoformat(),
            "estimatedDeliveryMinutes": 35,
            "estimatedArrivalTime": (now + timedelta(minutes=15)).isoformat(),
            "payment_status": "pending",
        },
        3: {
            "orderId": 3,
            "restaurantId": 101,
            "userId": 3,
            "items": [3],
            "status": "pending",
            "createdAt": (now - timedelta(minutes=5)).isoformat(),
            "estimatedDeliveryMinutes": 25,
            "estimatedArrivalTime": (now + timedelta(minutes=20)).isoformat(),
            "payment_status": "pending",
        },
    }

    response = client.get("/orders/restaurants/100/track-delivery")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["orderId"] == 1
    assert data[0]["status"] == "preparing"
    assert "estimatedArrivalTime" in data[0]
    assert "minutesRemaining" in data[0]
    assert data[1]["orderId"] == 2
    assert data[1]["status"] == "out-for-delivery"
    assert "estimatedArrivalTime" in data[1]
    assert "minutesRemaining" in data[1]

def test_track_delivery_for_restaurant_no_orders():
    """
    Should return empty list if restaurant has no orders.
    """
    database.orders_map.clear()

    response = client.get("/orders/restaurants/999/track-delivery")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_track_delivery_for_restaurant_excludes_other_restaurants_orders():
    """
    Should only return orders for the specified restaurant.
    """
    now = datetime.now()

    database.orders_map = {
        1: {
            "orderId": 1,
            "restaurantId": 100,
            "userId": 1,
            "items": [1],
            "status": "preparing",
            "createdAt": (now - timedelta(minutes=10)).isoformat(),
            "estimatedDeliveryMinutes": 40,
            "estimatedArrivalTime": (now + timedelta(minutes=30)).isoformat(),
            "payment_status": "pending",
        },
        2: {
            "orderId": 2,
            "restaurantId": 101,
            "userId": 2,
            "items": [2],
            "status": "out-for-delivery",
            "createdAt": (now - timedelta(minutes=20)).isoformat(),
            "estimatedDeliveryMinutes": 35,
            "estimatedArrivalTime": (now + timedelta(minutes=15)).isoformat(),
            "payment_status": "pending",
        },
    }

    response = client.get("/orders/restaurants/100/track-delivery")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["orderId"] == 1
    assert data[0]["status"] == "preparing"
