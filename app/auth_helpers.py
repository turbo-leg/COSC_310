"""Reusable authorization helpers for role-based access control."""

from fastapi import HTTPException
from app.database import get_user_by_id


def get_authenticated_user(user_id: int) -> dict:
    """
    Return the user if the user exists, raising 401 if the user is missing or invalid.
    """
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    return user


def require_authenticated_user(user_id: int) -> dict:
    """
    Helper for endpoints that only need a valid logged-in user.
    """
    return get_authenticated_user(user_id)


def require_admin(user_id: int) -> dict:
    """
    Ensure the user exists and has admin role.
    """
    user = get_authenticated_user(user_id)

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Admin access required"
        )

    return user


def check_admin_role(user: dict) -> None:
    """
    Check if a user dict has admin role. Raises 403 if not admin.
    """
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Admin access required"
        )


def require_restaurant_owner(user_id: int, restaurant_id: int) -> dict:
    """
    Ensure the user exists, is a restaurant owner, and owns the target restaurant.
    """
    user = get_authenticated_user(user_id)

    if user.get("role") != "restaurant":
        raise HTTPException(
            status_code=403,
            detail="Only the restaurant owner can access these endpoints"
        )

    owner_restaurant_id = user.get("restaurantId")
    # Backward compatibility: legacy data used userId as restaurant_id.
    if owner_restaurant_id is None:
        owner_restaurant_id = user.get("userId")

    if owner_restaurant_id != restaurant_id:
        raise HTTPException(
            status_code=403,
            detail="Only the restaurant owner can access these endpoints"
        )

    return user
