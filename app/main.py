"""
this is the main entry point for the FastAPI application
it initializes the in-memory storage from CSV, registers all route controllers,
and creates the FastAPI app instance that Uvicorn runs
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controllers import user_controller
from app.controllers import order_controller
from app.controllers import menu_controller
from app import database

@asynccontextmanager
async def lifespan(app_instance: FastAPI): # pylint: disable=unused-argument
    """
    Lifespan context manager to handle startup and shutdown events.
    """
    # Initialize in-memory storage from CSV at startup
    database.init_storage()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_controller.router)
app.include_router(order_controller.router)
app.include_router(menu_controller.router)


@app.get("/")
async def root():
    """
    Returns API message.
    """
    return {"message": "Lets go Sphixes"}
