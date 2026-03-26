"""
This file defines endpoints for menu-related logic.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from app.constants import UserRole
from app.database import (
    restaurant_exists,
    get_active_menu_for_restaurant,
    create_menu_item,
    update_menu_item,
    delete_menu_item,
    get_user_by_id,
    find_restaurants_by_food_item
)
from app.schemas import MenuItemResponse, MenuItemCreate, MenuItemUpdate

router = APIRouter(
    prefix="/restaurant",
    tags=["menu"],
)

def _verify_owner(user_id: int, restaurant_id: int):
    """
    Checks if user is owner of the restaurant.
    """
    if not user_id:
        raise HTTPException(
            status_code=403,
            detail="Only the restaurant owner can access these endpoints"
        )

    user = get_user_by_id(user_id)
    if (
        not user
        or user.get("role") != UserRole.RESTAURANT.value or
        user.get("userId") != restaurant_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the restaurant owner can access these endpoints"
        )

@router.get("/search", response_model=List[MenuItemResponse])
def search_food_items(query: str, skip: int = 0, limit: int = 100):
    """
    Search for food items across all restaurants.
    """
    return find_restaurants_by_food_item(query, skip=skip, limit=limit)

@router.get("/{restaurant_id}/menu", response_model=List[MenuItemResponse])
def get_restaurant_menu(restaurant_id: int, skip: int = 0, limit: int = 100):
    """
    Get active menu items for a specific restaurant.
    """
    if not restaurant_exists(restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return get_active_menu_for_restaurant(restaurant_id, skip=skip, limit=limit)

@router.post("/{restaurant_id}/menu", response_model=MenuItemResponse)
def add_menu_item(restaurant_id: int, item: MenuItemCreate, owner_id: int = None):
    """
    Add a new menu item.
    """
    _verify_owner(owner_id, restaurant_id)
    new_item = create_menu_item(restaurant_id, item.name, item.description, item.price)
    return new_item

@router.put("/{restaurant_id}/menu/{item_id}", response_model=MenuItemResponse)
def edit_menu_item(restaurant_id: int, item_id: int, item: MenuItemUpdate, owner_id: int = None):
    """
    Update a menu item.
    """
    _verify_owner(owner_id, restaurant_id)
    updated_item = update_menu_item(item_id, restaurant_id, item.model_dump(exclude_unset=True))
    if not updated_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated_item

@router.delete("/{restaurant_id}/menu/{item_id}")
def remove_menu_item(restaurant_id: int, item_id: int, owner_id: int = None):
    """
    Delete a menu item.
    """
    _verify_owner(owner_id, restaurant_id)
    success = delete_menu_item(item_id, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted"}
