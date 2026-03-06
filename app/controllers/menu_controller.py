"""
This file defines endpoints for menu-related logic.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from app.database import restaurant_exists, get_active_menu_for_restaurant
from app.schemas import MenuItemResponse

router = APIRouter(
    prefix="/restaurant",
    tags=["menu"],
)

@router.get("/{restaurant_id}/menu", response_model=List[MenuItemResponse])
def get_restaurant_menu(restaurant_id: int):
    """
    Get active menu items for a specific restaurant.
    """
    if not restaurant_exists(restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return get_active_menu_for_restaurant(restaurant_id)