"""
Controller for admin-specific endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

from app import database
from app.auth_helpers import require_admin
from app.services.admin_service import admin_service
from app.schemas import AdminStatsResponse, MenuItemResponse, PromoCreateRequest

class ToggleStockRequest(BaseModel):
    """Request payload for toggling stock status"""
    isActive: bool

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(
    user_id: int,
    start_date: Optional[str] = Query(None, description="Start date in ISO format"),
    end_date: Optional[str] = Query(None, description="End date in ISO format"),
    status: Optional[str] = Query(None, description="Order status filter")
):
    """
    Get system statistics. Admin only.
    """
    require_admin(user_id)
    return admin_service.get_stats(start_date=start_date, end_date=end_date, status=status)

@router.get("/menu", response_model=list[MenuItemResponse])
def get_all_menu_items_admin(user_id: int):
    """
    Get all menu items globally across all restaurants for admin management.
    """
    require_admin(user_id)
    return database.get_all_menu_items()

@router.put("/menu/{item_id}/toggle-stock", response_model=MenuItemResponse)
def toggle_menu_item_stock(user_id: int, item_id: int, payload: ToggleStockRequest):
    """
    This function will toggle the stock status of a menu item in the database.
    Only an admin is allowed to call this endpoint.
    """
    require_admin(user_id)

    target_item = database.get_menu_item_by_id(item_id)

    if target_item is None:
        print("Debug: The target item was None, returning 404")
        raise HTTPException(status_code=404, detail="Item not found in the database")
    update_data = {}
    update_data["isActive"] = payload.isActive

    updated_item_result = database.update_menu_item_admin(item_id, update_data)

    return updated_item_result

@router.post("/promo")
def create_promo(request: PromoCreateRequest, user_id: int):
    """
    Endpoint to create promo code data
    """
    require_admin(user_id)

    return admin_service.create_promo(
        code=request.code,
        discount=request.discount,
        expiry=request.expiry,
        assigned_users=request.assigned_users
    )
