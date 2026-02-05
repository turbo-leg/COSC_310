# This file manages in-memory user storage with CSV persistence
# users are loaded into a dictionary (map) at startup for O(1) lookup by ID
# I am not sure where to find the csv file is so we might need to adjut the path.
import csv
import os
from typing import Dict, Optional
CSV_FILE_PATH = "./users.csv" # Might need to adjust path
users_map: Dict[int, dict] = {}
next_id: int = 1

def load_users_from_csv(): 
   # Todo: Load users from CSV into the in-memory map
   pass


def save_users_to_csv():
   # Todo: Persist all users from the in-memory map to CSV
   pass


def init_storage():
   # Todo: Initialize storage by loading users from CSV
   pass


def get_all_users():
    # Todo: Return a list of users
    pass


def get_user_by_id(user_id: int):
    # Todo: Lookup user by ID in O(1) time
    pass


def get_user_by_email(email: str):
    # Todo: Lookup user by email
    pass

def create_user():
   # Todo: Create a new user and add it to the csv file using save_users_to_csv
   pass


def delete_user(user_id: int):
    #Todo: Delete a user by ID
    pass