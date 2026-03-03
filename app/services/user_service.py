"""
This file contains business logic for User operations
services handle CRUD operations and interact with the in-memory storage
controllers call these functions instead of accessing storage directly
so that means that its a way of abstracting the storage from the controllers
"""
from app.schemas import UserCreate
from app import database
from app.services.auth_service import auth_service



def get_users(skip: int = 0, limit: int = 100):
    """
    Gets users from database.
    """
    return database.get_all_users(skip=skip, limit=limit)

def get_user(user_id: int):
    """
    Gets one user by ID.
    """
    return database.get_user_by_id(user_id)

def get_user_by_email(email: str):
    """
    Gets one user by email.
    """
    return database.get_user_by_email(email)

def create_user(user: UserCreate):
    """
    Creates and Saves new user.
    """
    hashed_password = auth_service.hash_password(user.password)
    return database.create_user(
        name = user.name,
        email = user.email,
        password= hashed_password,
        role= "Regular User"
    )

def verify_user_login(email:str, password:str):
    """
    Verifies user login credentials.
    """
    return auth_service.login(email, password)

def delete_user(user_id: int):
    """
    Deletes user from database.
    """
    return database.delete_user(user_id)
