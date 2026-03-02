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
   # Saves all user data into a permanent CSV file.
   with open(CSV_FILE_PATH, mode = 'w', newline = '') as file:
      fieldNames = ["userId", "name", "email", "password", "role"]
      writer = csv.DictWriter(file, fieldnames = fieldNames)
      writer.writeheader()
      for user in users_map.values():
         writer.writerow(user)

def init_storage():
   # Todo: Initialize storage by loading users from CSV
   pass

def get_all_users():
    # Todo: Return a list of users
    pass

def get_user_by_id(user_id: int):
    # Todo: Lookup user by ID in O(1) time
    return users_map.get(user_id)

def get_user_by_email(email: str):
   # Todo: Lookup user by email
   for user in users_map.values():
      if user.get('email') == email:
         return user
   return None
   
def create_user(name: str, email: str, password:str, role:str):
   # Todo: Create a new user and add it to the csv file using save_users_to_csv
   global next_id
   new_user = {
      "userId": next_id,
      "name": name,
      "email": email,
      "password": password,
      "role": role
   }
   users_map[next_id] = new_user
   next_id += 1
   save_users_to_csv()
   return new_user
   
def delete_user(user_id: int):
    #Todo: Delete a user by ID
    pass