"""
Token management utilities."""

from jose import jwt, JWTError

SECRET = "secret123"

def create_token(user):
    """
    Creates a JWT token with the user's email and role.
    """
    return jwt.encode(
        {"email": user["email"], "role": user.get("role", "user")},
        SECRET,
        algorithm="HS256"
    )


def decode_token(token):
    """
    Verifies the token and returns the user information if valid.
    """
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except JWTError:
        return None
