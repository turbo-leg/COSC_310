"""
Fault Injection tests
"""
from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)

def test_database_corrupt():
    """
    Tests what happened when database is corrupted.
    """
    database.menu_items = None

    response = client.get("/menu")
    assert response.status_code == 404

    database.menu_items = []
