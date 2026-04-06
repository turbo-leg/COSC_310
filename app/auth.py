"""
Authentication utilities.
"""

from fastapi import Header, HTTPException
from app.database import get_user_by_email
from app.token import decode_token

BEARER_PREFIX = "Bearer "

def get_user(authorization: str = Header(default=None)):
    """
    Extract the authenticated user from the bearer token in the Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    if not authorization.startswith(BEARER_PREFIX):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = authorization.replace(BEARER_PREFIX, "", 1)
    token_data = decode_token(token)

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = get_user_by_email(token_data.get("email", ""))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
