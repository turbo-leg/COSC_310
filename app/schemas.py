"""
this file defines Pydantic schemas for request/response validation
schemas ensure API data is correctly typed and structured
they separate API contracts from database models for flexibility
"""
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base attributes for a user.
    """
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for user registration.
    """
    password: str = Field(..., min_length = 8, 
                          description= "Password must be at leat 8 characters long")

class UserLogin(BaseModel):
    """
    Schema for user login credentials.
    """
    email: EmailStr
    password: str

class UserResponse(UserBase):
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
