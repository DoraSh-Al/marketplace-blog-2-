from fastapi import FastAPI, HTTPException, Request

from src.api.articles import router as articles_router  # Добавляем
from src.api.auth import router as auth_router
from src.utils.auth import decode_access_token

app = FastAPI(title="Marketplace Blog API")

# Подключаем маршруты
app.include_router(auth_router)
app.include_router(articles_router)  # Добавляем

# Middleware для проверки токена
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")
    if token:
        try:
            decode_access_token(token)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token")
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
