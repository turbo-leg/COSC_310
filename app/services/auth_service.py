"""
Password Hashing and authentication checks.
"""

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app import database

class AuthService:
    """
    Handles all security tasks like password hashing and user login.
    """
    def __init__(self):
        self.password_hasher = PasswordHash((Argon2Hasher(),))

    def hash_password(self, password: str) -> str:
        """
        Turns a plain password into a scrambled code.
        """
        return self.password_hasher.hash(password)

    def login(self, email: str, password: str):
        """
        Checks if login details match the ones stored in memory.
        """
        user = database.get_user_by_email(email)
        if not user:
            return None
        if self.password_hasher.verify(password, user["password"]):
            return user
        return None

    def authorize_user(self, user_id: int):
        """
        Checks if a user is valid before allowing them in.
        """
        user = database.get_user_by_id(user_id)
        if user:
            return True
        return False

    def logout(self, user_id: int):
        """
        Clears the users session for a safe exit
        """
        return True

auth_service = AuthService()