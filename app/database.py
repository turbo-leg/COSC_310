"""
This file manages in-memory user storage with CSV persistence
users are loaded into a dictionary (map) at startup for O(1) lookup by ID
I am not sure where to find the csv file is so we might need to adjut the path.
"""
import csv
from typing import Dict
from sqlalchemy.ext.declarative import declarative_base
CSV_FILE_PATH = "./users.csv" # Might need to adjust path
MENU_CSV_FILE_PATH = "./menu_items.csv"
users_map: Dict[int, dict] = {}
menu_items: list[dict] = []
Base = declarative_base()
NEXT_ID: int = 1

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
    _ = skip
    _= limit

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


def load_menu_items_from_csv():
    """
    Loads menu items from CSV into memory.
    """
    global menu_items # pylint: disable=global-statement
    menu_items = []
    try:
        with open(MENU_CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                menu_items.append({
                    "itemId": int(row["itemId"]),
                    "restaurantId": int(row.get("restaurantId", row.get("restaurant_id", 0))),
                    "name": row["name"],
                    "description": row["description"],
                    "price": float(row["price"]),
                    "isActive": str(row.get("isActive", row.get("active", "true"))).lower() == "true"
                })
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
