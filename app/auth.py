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

    BEARER_PREFIX = "Bearer "
    token = authorization.replace(BEARER_PREFIX, "")
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
