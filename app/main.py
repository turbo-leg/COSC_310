# this is the main entry point for the FastAPI application
# it initializes the database, registers all route controllers,
# and creates the FastAPI app instance that Uvicorn runs
# I am wondering if we should make alembic migrations for the database or we can just use 
# the create_all() function to create the tables. I think we should use alembic migrations
# because it is more flexible and allows us to make changes to the database schema 
# without losing any data. But that might be overkill for this project. 
# Let me know what you think.
from fastapi import FastAPI
from app.database import engine, Base
from app.controllers import user_controller

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
