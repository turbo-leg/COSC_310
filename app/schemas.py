# this file defines Pydantic schemas for request/response validation
# schemas ensure API data is correctly typed and structured
# they separate API contracts from database models for flexibility
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str = Field(..., min_length = 8, description= "Password must be at leat 8 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    userId: int
    role: str
    class Config:
        from_attributes = True
