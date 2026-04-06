"""
this file defines Pydantic schemas for request/response validation
schemas ensure API data is correctly typed and structured
they separate API contracts from database models for flexibility
"""
from typing import List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.constants import UserRole, OrderStatus


class AdminStatsResponse(BaseModel):
    """
    Schema for Admin stats response.
    """
    total_users: int
    total_orders: int
    total_revenue: float
    total_menu_items: int


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


class MenuItemCreate(BaseModel):
    """
    Schema for creating a menu item.
    """
    name: str
    description: str
    price: float


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


class MenuItemUpdate(BaseModel):
    """
    Schema for updating a menu item.
    """
    name: str | None = None
    description: str | None = None
    price: float | None = None
    isActive: bool | None = None


class OrderModifyRequest(BaseModel):
    """
    Schema for modifying orders.
    """
    food_item : str | None = None
    order_value : float | None = None
    items : List[int] | None = None


class OrderCreateRequest(BaseModel):
    """
    Schema for creating a new order.
    """
    user_id: int
    restaurant_id: int
    items: List[int]
    time_minutes: int = 20
    distance_km: float = 5.0

class OrderResponse(BaseModel):
    """
    Schema for viewing incoming restaurant orders.
    """
    orderId: int
    restaurantId: int
    userId: int
    items: List[int] = []
    order_value: float = 0.0
    delivery_fee: float = 0.0
    total_cost: float = 0.0
    amount_paid: float = 0.0
    amount_due: float = 0.0
    wallet_applied: float = 0.0
    status: str
    payment_status: str = "pending"
    createdAt: str | None = None
    order_time: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PaymentRequest(BaseModel):
    """
    Schema for Payment Request.
    """
    order_id: int
    credit_card: str | None = None


class PaymentResponse(BaseModel):
    """
    Schema for Payment Delivery.
    """
    transaction_id: str
    message: str
    wallet_applied: float
    card_charged: float
    remaining_wallet_balance: float
    amount_due: float


class TrackOrderResponse(BaseModel):
    """
    Schema for tracking order status and ETA.
    """
    orderId: int
    status: OrderStatus
    estimatedArrivalTime: str
    minutesRemaining: int

class WalletTopUpRequest(BaseModel):
    """
    Schema for adding money to the customer's wallet.
    """
    amount: float = Field(..., gt=0)

class WalletBalanceResponse(BaseModel):
    """
    Schema for wallet balance response.
    """
    userId: int
    walletBalance: float

class UpdateOrderStatusRequest(BaseModel):
    """
    Schema for updating order status.
    """
    new_status: str


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
                          description= "Password must be at least 8 characters long")


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
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
