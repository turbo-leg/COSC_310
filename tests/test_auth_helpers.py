"""Tests for reusable authorization helpers."""

import pytest
from fastapi import HTTPException
from app import database
from app.auth_helpers import (
    require_authenticated_user,
    require_admin,
    require_restaurant_owner,
)


@pytest.fixture(autouse=True)
def reset_users():
    """Reset user storage before each test."""
    database.users_map = {
        1: {
            "userId": 1,
            "name": "Admin User",
            "email": "admin@test.com",
            "password": "pass",
            "role": "admin",
        },
        2: {
            "userId": 2,
            "name": "Restaurant Owner",
            "email": "owner@test.com",
            "password": "pass",
            "role": "restaurant",
        },
        3: {
            "userId": 3,
            "name": "Customer",
            "email": "customer@test.com",
            "password": "pass",
            "role": "Regular User",
        },
    }
    yield
    database.users_map = {}


def test_require_authenticated_user_success():
    """Valid user ID should return the user."""
    user = require_authenticated_user(1)
    assert user["userId"] == 1
    assert user["role"] == "admin"


def test_require_authenticated_user_missing_id():
    """Missing user ID should raise 401."""
    with pytest.raises(HTTPException) as exc:
        require_authenticated_user(None)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Authentication required"


def test_require_authenticated_user_invalid_user():
    """Unknown user ID should raise 401."""
    with pytest.raises(HTTPException) as exc:
        require_authenticated_user(999)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid user"


def test_require_admin_success():
    """Admin user should pass admin authorization."""
    user = require_admin(1)
    assert user["role"] == "admin"


def test_require_admin_forbidden_for_non_admin():
    """Non-admin should raise 403."""
    with pytest.raises(HTTPException) as exc:
        require_admin(3)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Forbidden: Admin access required"


def test_require_restaurant_owner_success():
    """Matching restaurant owner should pass."""
    user = require_restaurant_owner(2, 2)
    assert user["role"] == "restaurant"


def test_require_restaurant_owner_wrong_role():
    """Customer should not be allowed as restaurant owner."""
    with pytest.raises(HTTPException) as exc:
        require_restaurant_owner(3, 2)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Only the restaurant owner can access these endpoints"


def test_require_restaurant_owner_wrong_restaurant():
    """Restaurant owner should not access another restaurant's data."""
    with pytest.raises(HTTPException) as exc:
        require_restaurant_owner(2, 999)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Only the restaurant owner can access these endpoints"
