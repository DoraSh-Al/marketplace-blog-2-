from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Создаём движок для подключения к базе данных
engine = create_engine(settings.DATABASE_URL, echo=True)  # echo=True для отладки

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии в зависимостях FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
