"""
This file defines endpoints for menu-related logic.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.auth import require_restaurant
from app.database import (
    restaurant_exists,
    get_active_menu_for_restaurant,
    create_menu_item,
    update_menu_item,
    delete_menu_item,
)
from app.schemas import MenuItemResponse, MenuItemCreate, MenuItemUpdate

router = APIRouter(
    prefix="/restaurant",
    tags=["menu"],
)

def _verify_owner(user, restaurant_id: int):
    """
    Verifies that the user is the owner of the restaurant."""
    if user.get("role") != "restaurant" or user.get("userId") != restaurant_id:
        raise HTTPException(
            status_code=403,
            detail="Only the restaurant owner can access these endpoints"
        )

@router.get("/{restaurant_id}/menu", response_model=List[MenuItemResponse])
def get_restaurant_menu(restaurant_id: int):
    """
    Get active menu items for a specific restaurant.
    """
    if not restaurant_exists(restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return get_active_menu_for_restaurant(restaurant_id)

@router.post("/{restaurant_id}/menu", response_model=MenuItemResponse)
def add_menu_item(restaurant_id: int, item: MenuItemCreate, user=Depends(require_restaurant)):
    """
    Add a new menu item to the restaurant's menu."""
    _verify_owner(user, restaurant_id)
    return create_menu_item(restaurant_id, item.name, item.description, item.price)

@router.put("/{restaurant_id}/menu/{item_id}", response_model=MenuItemResponse)
def edit_menu_item(restaurant_id: int, item_id: int, item: MenuItemUpdate,
                   user=Depends(require_restaurant)):
    """
    Update a menu item.
    """
    _verify_owner(user, restaurant_id)
    updated_item = update_menu_item(item_id, restaurant_id, item.model_dump(exclude_unset=True))
    if not updated_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated_item

@router.delete("/{restaurant_id}/menu/{item_id}")
def remove_menu_item(restaurant_id: int, item_id: int, user=Depends(require_restaurant)):
    """
    Delete a menu item.
    """
    _verify_owner(user, restaurant_id)
    success = delete_menu_item(item_id, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted"}
