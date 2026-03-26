"""
This file defines REST API endpoints for User resources
controllers handle HTTP requests and delegate to services
each endpoint validates input, calls services, and returns responses
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import UserCreate, UserResponse, UserLogin
from app.services import user_service
from app.auth import get_user
from app.auth_helpers import check_admin_role


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(user=Depends(get_user)):
    """
    Returns the current logged in user's information.
    """
    return user

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100):
    """
    Retrieves list of all users.
    """
    return user_service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    """
    Retrieves one user by id.
    """
    user = user_service.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/")
def create_user(user: UserCreate):
    """
    This API endpoint signup new users and prevents duplicate emails.
    """
    db_user = user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user =  user_service.create_user(user=user)
    return {
        "message": "SUCCESSFUL",
        "user": {
            "name": new_user["name"],
            "email": new_user["email"]
    }
    }

@router.post("/login")
def login_user(credentials: UserLogin):
    """
    This API endpoint allows users to login with email and password.
    """
    user = user_service.verify_user_login(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid email or password"
        )
    return {
        "message" : "Login Successful",
        "user": {
            "email": credentials.email
        },
        "token": user
    }

@router.delete("/{user_id}")
def delete_user(user_id: int, user=Depends(get_user)):
    """
    Removes user by id.
    """
    check_admin_role(user)
    success = user_service.delete_user(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
