"""
this file defines Pydantic schemas for request/response validation
schemas ensure API data is correctly typed and structured
they separate API contracts from database models for flexibility
"""
from typing import List
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

class OrderResponse(BaseModel): # pylint: disable=too-few-public-methods
    """
    Schema for viewing incoming restaurant orders.
    """
    order_id: int
    restaurant_id: int
    food_item: str
    order_time: str
    order_value: float
    customer_id: int
    status: str

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

class MenuItemCreate(BaseModel):
    """
    Schema for creating a menu item.
    """
    name: str
    description: str
    price: float

class MenuItemUpdate(BaseModel):
    """
    Schema for updating a menu item.
    """
    name: str | None = None
    description: str | None = None
    price: float | None = None
    isActive: bool | None = None

class DeliveryRequest(BaseModel):
    """
    Schema for delivery request.
    """
    distance_km: float
    time_minutes: int


class DeliveryResponse(BaseModel):
    """
    Schema for delivery response.
    """
    cost: float

class TrackOrderResponse(BaseModel):
    """
    Schema for tracking order status and ETA.
    """
    orderId: int
    status: str
    estimatedArrivalTime: str
    minutesRemaining: int

class UpdateOrderStatusRequest(BaseModel):
    """
    Schema for updating order status.
    """
    new_status: str

class AdminStatsResponse(BaseModel):
    """
    Schema for Admin stats response.
    """
    total_users: int
    total_orders: int
    total_revenue: float
    total_menu_items: int
class OrderModifyRequest(BaseModel):
    """
    Schema for modifying orders.
    """
    food_item : str | None = None
    order_value : float | None = None
    items : List[int] | None = None

class PaymentRequest(BaseModel):
    """
    Schema for Payment Request.
    """
    order_id: int
    credit_card: str

class PaymentResponse(BaseModel):
    """
    Schema for Payment Delivery.
    """
    transaction_id: str
    message: str
