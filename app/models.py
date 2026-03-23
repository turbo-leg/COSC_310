""" 
This file defines SQLAlchemy ORM models
Each class represents a table, with columns as class attributes
Models map Python objects to database rows for easy CRUD operations
Lecture 9 - API Design, and REST architecture was helpful in understanding this
"""
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class User(Base): # pylint: disable=too-few-public-methods
    """
    users table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class Order(Base): # pylint: disable=too-few-public-methods
    """
    orders table
    """
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer)
    food_item = Column(String)
    order_time = Column(String)
    order_value = Column(Float)
    customer_id = Column(Integer)
