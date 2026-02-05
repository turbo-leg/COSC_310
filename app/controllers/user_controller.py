# This file defines REST API endpoints for User resources
# controllers handle HTTP requests and delegate to services
# each endpoint validates input, calls services, and returns responses
from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserResponse
from app.services import user_service 

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100):
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = user_service.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    db_user = user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(user=user)


@router.delete("/{user_id}")
def delete_user(user_id: int):
    success = user_service.delete_user(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
