"""
Handles delivery cost calculations.
"""
from app import database

def calculate_delivery_cost(distance_km: float, time_minutes: int) -> float:
    """
    Calculate delivery cost using distance and time.
    """

    base_fee = 5.0
    distance_rate = 0.5
    time_rate = 0.1
    # Rates can be adjusted based on business needs.
    # These are sample numbers for demonstration.

    cost = base_fee + (distance_km * distance_rate) + (time_minutes * time_rate)

    return round(cost, 2)

def assign_delivery(order_id: int, delivery_id: int):
    """
    Assign a delivery to an order.
    """
    return database.assign_delivery_to_order(order_id, delivery_id)
