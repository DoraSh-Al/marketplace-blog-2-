# Marketplace-blog-2-

API для блога маркетплейса, поддерживающее создание пользователей, статей, категорий и асинхронную отправку писем. Проект разработан в соответствии с макетом и требованиями задания.

## Технологии
- **Python 3.10**, **FastAPI** — для API
- **PostgreSQL** — база данных
- **RabbitMQ**, **Celery** — асинхронная отправка писем
- **MinIO** — хранилище изображений (в процессе интеграции)
- **Docker**, **Docker Compose** — контейнеризация
- **Poetry** — управление зависимостями
- **Ruff**, **Pre-commit** — линтеры
- **Pydantic Settings** — конфигурация

## Установка и запуск

### Требования
- Python 3.10+
- Poetry
- Docker и Docker Compose
- Git

### Локальная установка
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/DoraSh-Al/marketplace-blog-2-.git
   cd marketplace-blog-2
   ```

2. Установите Poetry (если ещё не установлено):
   ```bash
   pip install poetry
   ```

3. Установите зависимости:
   ```bash
   poetry install
   ```

4. Скопируйте `.env.example` в `.env` и настройте переменные:
   ```bash
   cp .env.example .env
   ```
   Пример `.env`:
   ```
   DATABASE_URL=postgresql://postgres:Noviigod1!@localhost:5433/blog_db
   RABBITMQ_URL=amqp://Dora:Noviigod1!@localhost:5672/
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=Dora
   MINIO_SECRET_KEY=Noviigod1!
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

5. Запустите FastAPI:
   ```bash
   poetry run uvicorn src.main:app --reload --port 8001
   ```

6. Запустите Celery-воркер для обработки писем:
   ```bash
   poetry run celery -A src.celery_app worker --loglevel=info --pool=solo
   ```

### Запуск через Docker
1. Убедитесь, что Docker и Docker Compose установлены.
2. Скопируйте `.env.example` в `.env` и настройте переменные (см. выше).
3. Запустите все сервисы:
   ```bash
   docker-compose up -d --build
   ```
   Это запустит:
   - FastAPI (`http://localhost:8001`)
   - PostgreSQL (порт 5433)
   - RabbitMQ (порты 5672, 15672)
   - MinIO (порты 9000, 9001)

4. Проверьте статус контейнеров:
   ```bash
   docker ps
   ```

5. Доступ к MinIO:
   - Откройте `http://localhost:9001`.
   - Логин: `Dora`, пароль: `Noviigod1!`.
   - Создайте бакет `images`.

## Эндпоинты
API доступно на `http://localhost:8001`. Основные эндпоинты:

- **POST /users/register** — Регистрация пользователя
  ```bash
  curl -X POST "http://localhost:8001/users/register" \
       -H "Content-Type: application/json" \
       -d '{"email": "test@example.com", "password": "test123"}'
  ```
  Ответ:
  ```json
  {
    "id": 1,
    "email": "test@example.com"
  }
  ```

- **GET /articles** — Список статей (поддерживает пагинацию и фильтры)
  ```bash
  curl "http://localhost:8001/articles?page_number=1&page_size=10&search=example"
  ```

- **POST /articles** — Создание статьи
  ```bash
  curl -X POST "http://localhost:8001/articles" \
       -H "Content-Type: application/json" \
       -d '{"title": "New Article", "content": "Content", "category_id": 1}'
  ```

- **GET /categories** — Список категорий
  ```bash
  curl "http://localhost:8001/categories"
  ```

- **POST /categories** — Создание категории
  ```bash
  curl -X POST "http://localhost:8001/categories" \
       -H "Content-Type: application/json" \
       -d '{"name": "New Category"}'
  ```

Полная документация доступна на `http://localhost:8001/docs` (Swagger UI).

## Тестирование
1. Установите зависимости для разработки:
   ```bash
   poetry install --with dev
   ```

2. Запустите тесты (в процессе разработки):
   ```bash
   poetry run pytest
   ```

## Разработка
- Линтеры: Используйте `ruff` для проверки кода:
  ```bash
  poetry run ruff check .
  ```
- Pre-commit: Проверяет код перед коммитом:
  ```bash
  poetry run pre-commit run --all-files
  ```

## TODO
- Настройка MinIO для загрузки изображений.
- Реализация логина и JWT-аутентификации.
- Хэширование паролей пользователей.
- Тесты для всех эндпоинтов.
- Финализация документации.

## Контакты
Разработчик: DoraSh-Al (dasasiraeva882@gmail.com)
