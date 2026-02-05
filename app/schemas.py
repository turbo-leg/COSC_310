# this file defines Pydantic schemas for request/response validation
# schemas ensure API data is correctly typed and structured
# they separate API contracts from database models for flexibility
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True
