"""
Test for delivery controller endpoints.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""
Dummy data for testing purposes.
"""
valid_delivery_1 = {
    "distance_km": 5,
    "time_minutes": 10
}

valid_delivery_2 = {
    "distance_km": 12,
    "time_minutes": 25
}

invalid_delivery = {
    "distance_km": 0,
    "time_minutes": 15
}

def test_delivery_price_valid_1():
    """
    Test delivery cost calculation with valid inputs. Returns cost greater than 0.
    """
    response = client.post("/delivery/cost", json=valid_delivery_1)

    assert response.status_code == 200
    data = response.json()

    assert "cost" in data
    assert data["cost"] > 0


def test_delivery_price_valid_2():
    """
    Test delivery cost calculation with valid inputs. Returns cost greater than 0 for a different delivery distance and time.
    """
    response = client.post("/delivery/cost", json=valid_delivery_2)

    assert response.status_code == 200
    data = response.json()

    assert data["cost"] > 0


def test_invalid_delivery_address():
    """
    Tests that an invalid delivery location returns a 400 error and an error message.
    """
    response = client.post("/delivery/cost", json=invalid_delivery)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid delivery address"
