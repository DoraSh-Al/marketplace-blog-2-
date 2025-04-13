import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_category(client: TestClient):
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={"email": "test15@example.com", "password": "test123"}
    )
    client.post(
        "/auth/login",
        json={"email": "test15@example.com", "password": "test123"}
    )
    response = client.post(
        "/categories",
        json={"name": "Tech"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Tech"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_categories(client: TestClient):
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={"email": "test16@example.com", "password": "test123"}
    )
    client.post(
        "/auth/login",
        json={"email": "test16@example.com", "password": "test123"}
    )
    client.post(
        "/categories",
        json={"name": "Tech"}
    )
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Tech"
