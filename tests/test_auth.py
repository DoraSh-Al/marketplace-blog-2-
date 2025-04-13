import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"email": "test9@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test9@example.com"

@pytest.mark.asyncio
async def test_register_duplicate_user(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "test10@example.com", "password": "test123"}
    )
    response = client.post(
        "/auth/register",
        json={"email": "test10@example.com", "password": "test123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_user(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "test11@example.com", "password": "test123"}
    )
    response = client.post(
        "/auth/login",
        json={"email": "test11@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Login successful"
    assert "access_token" in response.cookies

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
