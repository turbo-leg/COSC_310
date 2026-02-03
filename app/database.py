# this file configures the database connection using SQLAlchemy
# it creates the database engine
# this also uses a factory design pattern you can learn more about it here: https://refactoring.guru/design-patterns/factory-method
# the get_db() function provides database sessions to API endpoints
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# engine - Database connection pool
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# SessionLocal - Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base - Parent class all your models inherit from
Base = declarative_base()

# get_db() - Dependency injection for endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
