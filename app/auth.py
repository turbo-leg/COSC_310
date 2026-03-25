"""
Authentication utilities.
"""

from fastapi import Header, HTTPException, Depends
from app.token import decode_token

def get_user(authorization: str = Header(None)):
    """
    Extracts user information from the Authorization header and verifies the token.
    """
    if not authorization:
        raise HTTPException(status_code=401)

    token = authorization.replace("Bearer ", "")
    user = decode_token(token)

    if not user:
        raise HTTPException(status_code=401)

    return user

def require_admin(user= None):
    """
    Checks if the user has admin privileges.
    """
    if not user or not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_restaurant(user=Depends(get_user)):
    """"
    Checks if the user is a restaurant owner.
    """
    if user.get("role") != "restaurant":
        raise HTTPException(
            status_code=403,
            detail="Restaurant owner access required"
        )
    return user
