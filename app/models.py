""" 
This file defines SQLAlchemy ORM models
Each class represents a table, with columns as class attributes
Models map Python objects to database rows for easy CRUD operations
Lecture 9 - API Design, and REST architecture was helpful in understanding this
"""
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base): # pylint: disable=too-few-public-methods
    """
    users table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

#When we have our UML for M2, we can add more models here.
