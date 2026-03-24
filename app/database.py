"""
This file manages in-memory user storage with CSV persistence
users are loaded into a dictionary (map) at startup for O(1) lookup by ID
I am not sure where to find the csv file is so we might need to adjut the path.
"""
import csv
import datetime
from typing import Dict, List
import kagglehub
from sqlalchemy.orm import declarative_base
CSV_FILE_PATH = "./users.csv" # Might need to adjust path
MENU_CSV_FILE_PATH = "./menu_items.csv"
users_map: Dict[int, dict] = {}
menu_items: List[dict] = []
orders_map: Dict[int, dict] = {}
Base = declarative_base()
NEXT_ID: int = 1
NEXT_ORDER_ID: int = 1


def load_users_from_csv():
    """
    Todo: Load users from CSV into the in-memory map
    """

def save_users_to_csv():
    """
    Saves all user data into a permanent CSV file.
    """
    with open(CSV_FILE_PATH, mode = 'w', newline = '', encoding= 'utf-8') as file:
        field_names = ["userId", "name", "email", "password", "role"]
        writer = csv.DictWriter(file, fieldnames = field_names)
        writer.writeheader()
        for user in users_map.values():
            writer.writerow(user)

def init_storage():
    """
    Todo: Initialize storage by loading users from CSV
    """
    load_menu_items_from_csv()

def get_all_users(skip: int = 0, limit: int = 100):
    """
    Todo: Return a list of users
    """
    return list(users_map.values())[skip : skip + limit]

def get_user_by_id(user_id: int):
    """
    Quickly finds a user with their id number.
    """
    return users_map.get(user_id)

def get_user_by_email(email: str):
    """
    Lookup user by email
    """
    for user in users_map.values():
        if user.get('email') == email:
            return user
    return None

def create_user(name: str, email: str, password:str, role:str):
    """
    Creates a new user and add it to the csv file using save_users_to_csv
    """
    global NEXT_ID # pylint: disable=global-statement
    new_user = {
      "userId": NEXT_ID,
      "name": name,
      "email": email,
      "password": password,
      "role": role
   }
    users_map[NEXT_ID] = new_user
    NEXT_ID += 1
    save_users_to_csv()
    return new_user

def delete_user(user_id: int):
    """
    Todo: Delete a user by ID
    """
    _ = user_id


def download_dataset():
    """
    Downloads the Kaggle dataset and returns the local path
    """
    try:
        path = kagglehub.dataset_download("niszarkiah/food-delivery")
        return path
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Error downloading dataset: {e}")
        return None

def load_menu_items_from_csv():
    """
    This loads menu items from the Kaggle dataset into memory at startup
    """
    global menu_items # pylint: disable=global-statement
    menu_items = []
    dataset_path = download_dataset()
    if not dataset_path:
        return
    csv_file_path = f"{dataset_path}/food_delivery.csv"

    try:
        seen_items = set()
        item_counter = 1
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                restaurant_id = int(row.get("restaurant_id", 0))
                food_name = row.get("food_item", "Unknown Item")
                unique_identifier = f"{restaurant_id}_{food_name}"
                if unique_identifier not in seen_items:
                    seen_items.add(unique_identifier)
                    price = float(row.get("order_value", 10.0))
                    menu_items.append({
                        "itemId": item_counter,
                        "restaurantId": restaurant_id,
                        "name": food_name,
                        "description": f"Delicious {food_name}",
                        "price": price,
                        "isActive": True
                    })
                    item_counter += 1
    except FileNotFoundError:
        pass


def get_all_menu_items():
    """
    Returns all menu items in memory.
    """
    return menu_items


def get_menu_item_by_id(item_id: int):
    """
    Returns one menu item by item id.
    """
    for item in menu_items:
        if item["itemId"] == item_id:
            return item
    return None


def restaurant_exists(restaurant_id: int):
    """
    Returns True when at least one menu item belongs to the restaurant.
    """
    for item in menu_items:
        if item.get("restaurantId") == restaurant_id:
            return True
    return False


def get_active_menu_for_restaurant(restaurant_id: int):
    """
    Returns active menu items for one restaurant.
    """
    return [
        item for item in menu_items
        if item.get("restaurantId") == restaurant_id and item.get("isActive", True)
    ]

def find_restaurants_by_food_item(food_name: str):
    """
    Returns restaurants with the inputted food name. Only menu items with the food name are returned
    """
    food = food_name.strip().lower()
    results = {}
    for item in menu_items:
        if not item.get("isActive"):
            continue
        item_name = item.get("name", "").strip().lower()
        if food in item_name:
            restaurant_id = item.get("restaurantId")
            if restaurant_id not in results:
                results[restaurant_id] = []
            results[restaurant_id].append(item)
    return results
def create_order(user_id: int, restaurant_id: int, items: list, time_minutes: int = 20):
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

    new_order = {
        "orderId": NEXT_ORDER_ID,
        "userId": user_id,
        "restaurantId": restaurant_id,
        "items": items,
        "status": "pending",
        "createdAt": created_at.isoformat(),
        "estimatedDeliveryMinutes": estimated_delivery_minutes,
        "estimatedArrivalTime": estimated_arrival_time.isoformat(),
        "payment_status": "pending",
        "notifications": [],
        "latestNotification": None,
        "customerNotified": False
    }

    orders_map[NEXT_ORDER_ID] = new_order
    NEXT_ORDER_ID += 1
    return new_order

def get_order_by_id(order_id: int):
    """
    Returns an order by its ID.
    """
    return orders_map.get(order_id)

def update_order_status(order_id: int, new_status: str):
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

def get_incoming_orders_for_restaurant(restaurant_id: int):
    """
    Returns incoming orders for a specific restaurant.
    """
    return [
        order for order in orders_map.values()
        if order["restaurantId"] == restaurant_id
    ]

def get_all_orders():
    """
    Returns all orders in memory.
    """
    return list(orders_map.values())

def create_menu_item(restaurant_id: int, name: str, description: str, price: float):
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

def update_menu_item(item_id: int, restaurant_id: int, updates: dict):
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

def delete_menu_item(item_id: int, restaurant_id: int):
    """
    Deletes an existing menu item.
    """
    for i, item in enumerate(menu_items):
        if item["itemId"] == item_id and item["restaurantId"] == restaurant_id:
            del menu_items[i]
            return True
    return False

def update_payment_status(order_id: int, new_status: str):
    """
    Updates payment status of an order.
    """
    order = orders_map.get(order_id)

    if not order:
        return None

    order["payment_status"] = new_status
    return order

def cancel_order_in_database(order_id: int) -> dict:
    """
    Marks an order as status = `cancelled` in db.
    """
    if order_id in orders_map:
        orders_map[order_id]["status"] = "cancelled"
        return orders_map[order_id]
    return None

def modify_order_in_database(order_id: int, modify_data: dict) -> dict:
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
    Calculates total revenue from accepted payments for a restaurant.
    """
    total = 0.0
    for order in orders_map.values():
        if order.get("restaurantId") == restaurant_id and order.get("payment_status") == "accepted":
            total += order.get("order_value", 0.0)
    return total
