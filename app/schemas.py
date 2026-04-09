"""
this file defines Pydantic schemas for request/response validation
schemas ensure API data is correctly typed and structured
they separate API contracts from database models for flexibility
"""
from typing import List
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
from app.constants import UserRole, OrderStatus, RefundReason, RefundStatus


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
    credit_card: str = Field(
        ...,
        min_length=16,
        max_length=16,
        description="16-digit card number used to simulate top-up funding",
    )

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


class RefundCreateRequest(BaseModel):
    """
    Schema for creating a refund request.
    """
    user_id: int
    reason: RefundReason
    description: str = Field(..., min_length=10, max_length=500)


class RefundResponse(BaseModel):
    """
    Schema for refund request response.
    """
    refundId: int
    orderId: int
    userId: int
    reason: str
    description: str
    status: RefundStatus
    createdAt: str

    model_config = ConfigDict(from_attributes=True)


class RefundUpdateRequest(BaseModel):
    """
    Schema for admin to approve or deny a refund.
    """
    status: RefundStatus


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
    role: UserRole = UserRole.REGULAR_USER
    restaurantId: int | None = None

    @model_validator(mode="after")
    def validate_role_restaurant(self):
        """
        Check if role is correct based on input.
        """
        if self.role == UserRole.RESTAURANT and self.restaurantId is None:
            raise ValueError("restaurantId is required when role is restaurant")
        if self.role != UserRole.RESTAURANT and self.restaurantId is not None:
            raise ValueError("restaurantId can only be set when role is restaurant")
        if self.role == UserRole.ADMIN:
            raise ValueError("admin role cannot be chosen at registration")
        return self


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

class PromoCreateRequest(BaseModel):
    """
    Schema for creating promo request
    """
    code: str
    discount: float
    expiry: str
    assigned_users: List[int] | None = None


class ApplyPromoRequest(BaseModel):
    """
    Schema for applying promo request
    """
    code: str
    user_id: int
