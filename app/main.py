"""
this is the main entry point for the FastAPI application
it initializes the in-memory storage from CSV, registers all route controllers,
and creates the FastAPI app instance that Uvicorn runs
"""
from fastapi import FastAPI
from app import database
from app.controllers import user_controller
#Todo : Initialize in-memory storage from CSV at startup database.init_storage() after it is implemented

app = FastAPI()

app.include_router(user_controller.router)

@app.get("/")
async def root():
    """
    Returns API message.
    """
    return {"message": "Lets go Sphixes"}
