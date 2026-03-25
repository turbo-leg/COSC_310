"""
Testing for assigning deliveries to orders.
"""

from app import database
from app.services.delivery_service import assign_delivery

def test_assign_delivery_success():
    """
    Test assigning a delivery to a valid order.
    """

    # dummy data
    order = database.create_order(
        user_id=1,
        restaurant_id=101,
        items=[1, 2],
        time_minutes=20
    )

    order_id = order["orderId"]

    # assign delivery
    updated_order = assign_delivery(order_id, delivery_id=555)

    # assertions
    assert updated_order is not None
    assert updated_order["deliveryId"] == 555
    assert updated_order["status"] == "assigned"


def test_assign_delivery_invalid_order():
    """
    Test assigning delivery to non-existent order.
    """

    result = assign_delivery(order_id=9999, delivery_id=123)

    assert result is None
