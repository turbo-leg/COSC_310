"""
this file defines Pydantic schemas for request/response validation
schemas ensure API data is correctly typed and structured
they separate API contracts from database models for flexibility
"""
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel): # pylint: disable=too-few-public-methods
    """
    Base attributes for a user.
    """
    name: str
    email: EmailStr

class UserCreate(UserBase): # pylint: disable=too-few-public-methods
    """
    Schema for user registration.
    """
    password: str = Field(..., min_length = 8,
                          description= "Password must be at leat 8 characters long")

class UserLogin(BaseModel): # pylint: disable=too-few-public-methods
    """
    Schema for user login credentials.
    """
    email: EmailStr
    password: str

class UserResponse(UserBase): # pylint: disable=too-few-public-methods
    """
    Schema for API user response.
    """
    userId: int
    role: str
    class Config: # pylint: disable=too-few-public-methods
        """
        DocString
        """
        from_attributes = True

class MenuItemResponse(BaseModel):
    """
    Schema for menu item response.
    """
    itemId: int
    restaurantId: int
    name: str
    description: str
    price: float
    isActive: bool
