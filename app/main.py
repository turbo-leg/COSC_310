"""
this is the main entry point for the FastAPI application
it initializes the in-memory storage from CSV, registers all route controllers,
and creates the FastAPI app instance that Uvicorn runs
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controllers import (
    user_controller, menu_controller, delivery_controller,
    order_controller, admin_controller, payment_controller
)
from app import database

@asynccontextmanager
async def lifespan(app_instance: FastAPI): # pylint: disable=unused-argument
    """
    Lifespan context manager to handle startup and shutdown events.
    """
    # Initialize in-memory storage from CSV at startup
    database.init_storage()
    # Startup complete
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_controller.router)
app.include_router(menu_controller.router)
app.include_router(delivery_controller.router)
app.include_router(order_controller.router)
app.include_router(admin_controller.router)
app.include_router(payment_controller.router)


@app.get("/restaurants", response_model=list)
def get_restaurants(skip: int = 0, limit: int = 100, query: str = None):
    """
    Retrieves all restaurants, optionally filtered by name.
    """
    restaurants = database.get_all_restaurants(skip=skip, limit=limit)
    if query:
        restaurants = [r for r in restaurants if query.lower() in r.get("name", "").lower()]
    return restaurants


@app.get("/")
async def root():
    """
    Returns API message.
    """
    return {"message": "Lets go Sphixes"}
