"""
Testing for the authentication logic.
"""
from fastapi.testclient import TestClient
from app import database
from app.main import app
from app.auth import get_user

client = TestClient(app)

def test_successful_registration():
    """
    Checks if regristration logic works.
    """
    fake_data = {
        "name": "Test user",
        "email": "testuser@gmail.com",
        "password":"testuserpassword"
    }

    response = client.post("/users", json=fake_data)
    assert response.status_code == 200
    assert response.json()["message"] == "SUCCESSFUL"
    assert response.json()["user"]["email"] == "testuser@gmail.com"

def test_duplicate_registration():
    """
    Checks if email duplicate catch logic works.
    """
    fake_data = {
        "name": "Test user",
        "email": "testuser@gmail.com",
        "password":"testuserpassword"
    }

    response = client.post("/users", json=fake_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_successful_login():
    """
    Checks if login logic works.
    """
    fake_data = {
        "email": "testuser@gmail.com",
        "password":"testuserpassword"
    }
    response = client.post("/users/login", json=fake_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Login Successful"
    assert "token" in response.json()

def test_failed_login():
    """
    Checks if bad login logic works.
    """
    fake_data = {
        "email": "testuser@gmail.com",
        "password":"karibou"
    }
    response = client.post("/users/login", json=fake_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_password_too_short():
    """
    Checks if password rule logic works.
    """
    fake_data = {
        "name": "Test user",
        "email": "testuser@gmail.com",
        "password":"123"
    }
    response = client.post("/users", json=fake_data)
    assert response.status_code == 422
    assert "password" in response.text

def test_me_requires_token():
    """
    Should fail if no token is provided.
    """
    response = client.get("/users/me")
    assert response.status_code == 401

def test_me_with_token():
    """
    Should work with valid token.
    """
    login = client.post("/users/login", json={
        "email": "testuser@gmail.com",
        "password": "testuserpassword"
    })

    token = login.json()["token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_delete_user_as_admin():
    """Admin should be able to delete a user by ID."""
    # create a user first
    fake_data = {
        "name": "Delete Me",
        "email": "deleteme@gmail.com",
        "password": "deletemepassword"
    }
    create_response = client.post("/users", json=fake_data)
    assert create_response.status_code == 200

    created_user = database.get_user_by_email("deleteme@gmail.com")
    assert created_user is not None
    user_id = created_user["userId"]

    # override auth dependency to simulate an admin
    app.dependency_overrides[get_user] = lambda: {
        "email": "admin@gmail.com",
        "role": "admin",
        "is_admin": True
    }

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted"

    # confirm user is really gone
    assert database.get_user_by_id(user_id) is None

    read_response = client.get(f"/users/{user_id}")
    assert read_response.status_code == 404
    assert read_response.json()["detail"] == "User not found"

    app.dependency_overrides.clear()
