"""
This file manages in-memory user storage with CSV persistence
users are loaded into a dictionary (map) at startup for O(1) lookup by ID
I am not sure where to find the csv file is so we might need to adjut the path.
"""
import csv
import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import declarative_base
from app.constants import OrderStatus, PaymentStatus, RefundStatus
CSV_FILE_PATH = "./users.csv" # Might need to adjust path
MENU_CSV_FILE_PATH = "./menu_items.csv"
users_map: Dict[int, dict] = {}
menu_items: List[dict] = []
orders_map: Dict[int, dict] = {}
refunds_map: Dict[int, dict] = {}
Base = declarative_base()
NEXT_ID: int = 1
NEXT_ORDER_ID: int = 1
NEXT_REFUND_ID: int = 1


def load_users_from_csv() -> None:
    """
    Todo: Load users from CSV into the in-memory map
    """
    global users_map, NEXT_ID  # pylint: disable=global-statement

    users_map = {}

    try:
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_id = int(row["userId"])
                row["userId"] = user_id
                restaurant_id_raw = row.get("restaurantId")
                if restaurant_id_raw in (None, ""):
                    # Back-compat: historically restaurant owners used userId as restaurant_id
                    row["restaurantId"] = user_id if row.get("role") == "restaurant" else None
                else:
                    row["restaurantId"] = int(restaurant_id_raw)
                users_map[user_id] = row

            if users_map:
                NEXT_ID = max(users_map.keys()) + 1
            else:
                NEXT_ID = 1

    except FileNotFoundError:
        users_map = {}
        NEXT_ID = 1

def save_users_to_csv():
    """
    Saves all user data into a permanent CSV file.
    """
    with open(CSV_FILE_PATH, mode = 'w', newline = '', encoding= 'utf-8') as file:
        field_names = ["userId", "name", "email", "password", "role", "restaurantId"]
        writer = csv.DictWriter(file, fieldnames = field_names)
        writer.writeheader()
        for user in users_map.values():
            row = dict(user)
            if row.get("restaurantId") is None:
                row["restaurantId"] = ""
            writer.writerow(row)

def init_storage() -> None:
    """
    Todo: Initialize storage by loading users from CSV
    """
    load_users_from_csv()
    load_menu_items_from_csv()

def get_all_users(skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Todo: Return a list of users
    """
    return list(users_map.values())[skip : skip + limit]

def get_all_restaurants(skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Returns one row per distinct restaurant that appears in menu data.
    Display name is Restaurant {id} (not tied to owner user display names).
    userId mirrors restaurantId for routes that still use /restaurant/{id}.
    """
    restaurant_ids = sorted(
        {
            int(item["restaurantId"])
            for item in menu_items
            if item.get("restaurantId") is not None
        }
    )
    restaurants = [
        {
            "restaurantId": rid,
            "userId": rid,
            "name": f"Restaurant {rid}",
            "role": "restaurant",
        }
        for rid in restaurant_ids
    ]
    return restaurants[skip : skip + limit]

def search_restaurants_by_name(query: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Returns menu-derived restaurants whose display name or id matches the query.
    """
    q = query.strip().lower()
    all_rows = get_all_restaurants(skip=0, limit=10000)
    restaurants = [
        r for r in all_rows
        if q in r.get("name", "").lower()
        or q in str(r.get("restaurantId", ""))
    ]
    return restaurants[skip : skip + limit]

def get_user_by_id(user_id: int) -> Optional[dict]:
    """
    Quickly finds a user with their id number.
    """
    return users_map.get(user_id)

def get_user_by_email(email: str) -> Optional[dict]:
    """
    Lookup user by email
    """
    for user in users_map.values():
        if user.get('email') == email:
            return user
    return None

def create_user(
    name: str,
    email: str,
    password: str,
    role: str,
    restaurant_id: int | None = None
) -> dict:
    """
    Creates a new user and add it to the csv file using save_users_to_csv
    """
    global NEXT_ID # pylint: disable=global-statement
    new_user = {
      "userId": NEXT_ID,
      "name": name,
      "email": email,
      "password": password,
      "role": role,
      "restaurantId": restaurant_id
   }
    users_map[NEXT_ID] = new_user
    NEXT_ID += 1
    save_users_to_csv()
    return new_user

def get_restaurant_owner(restaurant_id: int) -> Optional[dict]:
    """
    Returns the restaurant owner for a restaurant_id, if any.
    """
    for user in users_map.values():
        if user.get("role") == "restaurant" and user.get("restaurantId") == restaurant_id:
            return user
    return None

def delete_user(user_id: int) -> bool:
    """Delete a user by ID and persist the updated data."""
    if user_id not in users_map:
        return False

    del users_map[user_id]
    save_users_to_csv()
    return True

def read_menu_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Reads Menu csv file and returns raw rows.
    """
    try:
        with open(file=file_path, mode='r', newline= '', encoding= 'utf-8')as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

def process_rows(rows: List[Dict[str, str]]) -> List[Dict]:
    """
    Processes raw CSV rows into structured menu items (deduplicated).
    """
    processed_items: List[dict] = []
    seen_items = set()
    item_counter = 1

    for row in rows:
        restaurant_id = int(row.get("restaurant_id", 0))
        food_name = row.get("food_item", "Unknown Item")

        unique_identifier = f"{restaurant_id}_{food_name}"

        if unique_identifier in seen_items:
            continue

        seen_items.add(unique_identifier)

        price = float(row.get("order_value", 10.0))

        processed_items.append({
            "itemId": item_counter,
            "restaurantId": restaurant_id,
            "name": food_name,
            "description": f"Delicious {food_name}",
            "price": price,
            "isActive": True
        })

        item_counter += 1

    return processed_items

def load_menu_items_from_csv() -> None:
    """
    This loads menu items from the local CSV file into memory at startup
    """
    global menu_items # pylint: disable=global-statement
    rows = read_menu_csv(MENU_CSV_FILE_PATH)
    menu_items = process_rows(rows)


def get_all_menu_items() -> List[dict]:
    """
    Returns all menu items in memory.
    """
    return menu_items


def get_menu_item_by_id(item_id: int) -> Optional[dict]:
    """
    Returns one menu item by item id.
    """
    for item in menu_items:
        if item["itemId"] == item_id:
            return item
    return None


def restaurant_exists(restaurant_id: int) -> bool:
    """
    Returns True when at least one menu item belongs to the restaurant.
    """
    for item in menu_items:
        if item.get("restaurantId") == restaurant_id:
            return True
    return False


def get_active_menu_for_restaurant(restaurant_id: int, skip: int = 0, limit: int = 100
) -> List[dict]:
    """
    Returns active menu items for one restaurant.
    """
    items = [
        item for item in menu_items
        if item.get("restaurantId") == restaurant_id and item.get("isActive", True)
    ]
    return items[skip : skip + limit]

def find_restaurants_by_food_item(food_name: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Returns menu items with the inputted food name (paginated).
    """
    food = food_name.strip().lower()
    results = []
    for item in menu_items:
        if not item.get("isActive"):
            continue
        item_name = item.get("name", "").strip().lower()
        if food in item_name:
            results.append(item)
    return results[skip : skip + limit]
def create_order(user_id: int, restaurant_id: int, items: list, time_minutes: int = 20) -> dict:
    """
    Creates a new order and stores it in memory, with ETA Tracking.
    """
    global NEXT_ORDER_ID  # pylint: disable=global-statement

    created_at = datetime.datetime.now()
    # 15 minutes for restaurant prep, 5 minutes for pickup,
    # plus the inputted time for delivery
    estimated_delivery_minutes = 15 + 5 + time_minutes
    estimated_arrival_time = created_at + datetime.timedelta(
        minutes=estimated_delivery_minutes)
    total_value = 0.0
    for item_id in items:
        item = get_menu_item_by_id(item_id)
        if item:
            total_value += item.get("price", 0.0)

    new_order = {
        "orderId": NEXT_ORDER_ID,
        "userId": user_id,
        "restaurantId": restaurant_id,
        "items": items,
        "order_value": total_value,
        "status": OrderStatus.PENDING.value,
        "createdAt": created_at.isoformat(),
        "estimatedDeliveryMinutes": estimated_delivery_minutes,
        "estimatedArrivalTime": estimated_arrival_time.isoformat(),
        "payment_status": PaymentStatus.UNPAID.value,
        "notifications": [],
        "latestNotification": None,
        "customerNotified": False
    }

    orders_map[NEXT_ORDER_ID] = new_order
    NEXT_ORDER_ID += 1
    return new_order

def get_order_by_id(order_id: int) -> Optional[dict]:
    """
    Returns an order by its ID.
    """
    return orders_map.get(order_id)

def update_order_status(order_id: int, new_status: str) -> Optional[dict]:
    """
    Updates the status of an existing order.
    """
    order = orders_map.get(order_id)
    if not order:
        return None

    old_status = order["status"]

    # Do not notify customer if the status does not change
    if old_status == new_status:
        order["customerNotified"] = False
        order["latestNotification"] = None
        return order

    order["status"] = new_status

    notification = {
        "orderId": order["orderId"],
        "userId": order["userId"],
        "oldStatus": old_status,
        "newStatus": new_status,
        "message": (
            f"Your order #{order['orderId']} status has changed from "
            f"{old_status} to {new_status}."
        ),
        "sentAt": datetime.datetime.now().isoformat()
    }
    order["notifications"].append(notification)
    order["latestNotification"] = notification
    order["customerNotified"] = True
    return order

def get_incoming_orders_for_restaurant(restaurant_id: int) -> List[dict]:
    """
    Returns incoming orders for a specific restaurant.
    """
    return [
        order for order in orders_map.values()
        if order["restaurantId"] == restaurant_id
    ]

def get_orders_for_user(user_id: int) -> List[dict]:
    """
    Returns all orders for a specific user.
    """
    return [
        order for order in orders_map.values()
        if order.get("userId") == user_id
    ]

def get_all_orders() -> List[dict]:
    """
    Returns all orders in memory.
    """
    return list(orders_map.values())

def create_menu_item(restaurant_id: int, name: str, description: str, price: float) -> dict:
    """
    Creates a new menu item for the given restaurant.
    """
    new_id = max((item["itemId"] for item in menu_items), default=0) + 1
    new_item = {
        "itemId": new_id,
        "restaurantId": restaurant_id,
        "name": name,
        "description": description,
        "price": price,
        "isActive": True
    }
    menu_items.append(new_item)
    return new_item

def update_menu_item(item_id: int, restaurant_id: int, updates: dict) -> Optional[dict]:
    """
    Updates an existing menu item.
    """
    for item in menu_items:
        if item["itemId"] == item_id and item["restaurantId"] == restaurant_id:
            for key, value in updates.items():
                if value is not None:
                    item[key] = value
            return item
    return None

def delete_menu_item(item_id: int, restaurant_id: int) -> bool:
    """
    Deletes an existing menu item.
    """
    for i, item in enumerate(menu_items):
        if item["itemId"] == item_id and item["restaurantId"] == restaurant_id:
            del menu_items[i]
            return True
    return False

def update_payment_status(order_id: int, new_status: str) -> Optional[dict]:
    """
    Updates payment status of an order.
    """
    order = orders_map.get(order_id)

    if not order:
        return None

    order["payment_status"] = new_status
    return order

def assign_delivery_to_order(order_id: int, delivery_id: int) -> Optional[dict]:
    """
    Assigns a delivery driver to an order.
    """
    order = orders_map.get(order_id)

    if not order:
        return None

    order["deliveryId"] = delivery_id
    order["status"] = OrderStatus.ASSIGNED.value

    return order
def cancel_order_in_database(order_id: int) -> Optional[dict]:
    """
    Marks an order as status = `cancelled` in db.
    """
    if order_id in orders_map:
        orders_map[order_id]["status"] = OrderStatus.CANCELLED.value
        return orders_map[order_id]
    return None

def modify_order_in_database(order_id: int, modify_data: dict) -> Optional[dict]:
    """
    Modify specific values in the order.
    """
    if order_id in orders_map:
        for key, value in modify_data.items():
            if value is not None:
                orders_map[order_id][key] = value
        return orders_map[order_id]
    return None

def get_restaurant_revenue(restaurant_id: int) -> float:
    """
    Calculates total revenue from accepted payments minus approved refunds.
    """
    total = 0.0
    for order in orders_map.values():
        if (
            order.get("restaurantId") == restaurant_id
            and order.get("payment_status") in (PaymentStatus.ACCEPTED.value, "paid")
        ):
            total += order.get("order_value", 0.0)
    for refund in refunds_map.values():
        if refund.get("status") == RefundStatus.APPROVED.value:
            order = orders_map.get(refund.get("orderId"))
            if order and order.get("restaurantId") == restaurant_id:
                total -= order.get("order_value", 0.0)
    return max(total, 0.0)


def create_refund(order_id: int, user_id: int, reason: str, description: str) -> dict:
    """
    Creates a new refund request stored in memory.
    """
    global NEXT_REFUND_ID  # pylint: disable=global-statement
    new_refund = {
        "refundId": NEXT_REFUND_ID,
        "orderId": order_id,
        "userId": user_id,
        "reason": reason,
        "description": description,
        "status": RefundStatus.PENDING.value,
        "createdAt": datetime.datetime.now().isoformat(),
    }
    refunds_map[NEXT_REFUND_ID] = new_refund
    NEXT_REFUND_ID += 1
    return new_refund


def get_refund_by_order_id(order_id: int) -> Optional[dict]:
    """
    Returns the refund request for a given order, if any.
    """
    for refund in refunds_map.values():
        if refund.get("orderId") == order_id:
            return refund
    return None


def get_all_refunds() -> List[dict]:
    """
    Returns all refund requests in memory.
    """
    return list(refunds_map.values())


def get_refunds_for_user(user_id: int) -> List[dict]:
    """
    Returns all refund requests submitted by a specific user.
    """
    return [r for r in refunds_map.values() if r.get("userId") == user_id]


def update_refund_status(refund_id: int, new_status: str) -> Optional[dict]:
    """
    Updates the status of a refund request (approved or denied).
    """
    refund = refunds_map.get(refund_id)
    if not refund:
        return None
    refund["status"] = new_status
    return refund
