"""
This file manages in-memory user storage with CSV persistence
users are loaded into a dictionary (map) at startup for O(1) lookup by ID
I am not sure where to find the csv file is so we might need to adjut the path.
"""
import csv
from typing import Dict
from sqlalchemy.ext.declarative import declarative_base
CSV_FILE_PATH = "./users.csv" # Might need to adjust path
users_map: Dict[int, dict] = {}
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
