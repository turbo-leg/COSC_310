"""
Testing for the authentication logic.
"""
from fastapi.testclient import TestClient
from app.main import app

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
