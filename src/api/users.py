from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserOut
from src.tasks import send_email

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Проверка существующего пользователя
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Хешируем пароль
        hashed_password = pwd_context.hash(user.password)
        db_user = User(email=user.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Отправка email
        try:
            send_email.delay(
                to_email=user.email,
                subject="Добро пожаловать!",
                body=f"Привет, {user.email}! Спасибо за регистрацию в нашем блоге."
            )
        except Exception as e:
            print(f"Failed to send email: {str(e)}")  # Логируем, не прерываем

        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
