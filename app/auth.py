"""
Authentication utilities.
"""

from fastapi import Header, HTTPException
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

from fastapi import HTTPException

def require_admin(user= None):
    if not user or not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

