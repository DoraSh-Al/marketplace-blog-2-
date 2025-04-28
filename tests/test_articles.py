import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_article(client: TestClient, db):
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={"email": "test12@example.com", "password": "test123"}
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "test12@example.com", "password": "test123"}
    )
    assert login_response.status_code == 200

    # Создание категории
    category_response = client.post(
        "/categories",
        json={"name": "Tech"}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    # Создание статьи
    response = client.post(
        "/articles",
        data={
            "title": "Test Article",
            "content": "Content",
            "category_id": str(category_id)
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["category_id"] == category_id
    assert data["image_url"] is None
    assert "created_at" in data
    assert "updated_at" in data
    assert "id" in data

@pytest.mark.asyncio
async def test_get_articles(client: TestClient, db):
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={"email": "test13@example.com", "password": "test123"}
    )
    client.post(
        "/auth/login",
        json={"email": "test13@example.com", "password": "test123"}
    )
    # Создание категории
    client.post(
        "/categories",
        json={"name": "Tech"}
    )
    # Создание статьи
    client.post(
        "/articles",
        data={
            "title": "Test Article",
            "content": "Content",
            "category_id": "1"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response = client.get("/articles?search=Test&page_number=1&page_size=5")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Test Article"
    assert response.json()[0]["image_url"] is None

@pytest.mark.asyncio
async def test_delete_article(client: TestClient, db):
    # Регистрация и логин
    client.post(
        "/auth/register",
        json={"email": "test14@example.com", "password": "test123"}
    )
    client.post(
        "/auth/login",
        json={"email": "test14@example.com", "password": "test123"}
    )
    # Создание категории
    client.post(
        "/categories",
        json={"name": "Tech"}
    )
    # Создание статьи
    article_response = client.post(
        "/articles",
        data={
            "title": "Test Article",
            "content": "Content",
            "category_id": "1"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    article_id = article_response.json()["id"]
    response = client.delete(f"/articles/{article_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "Article deleted"
