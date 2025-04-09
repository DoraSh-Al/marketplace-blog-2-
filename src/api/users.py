from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserOut
from src.tasks import send_email

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(email=user.email, password=user.password)  # Хэшируй пароль в продакшене
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    send_email.delay(
        to_email=user.email,
        subject="Добро пожаловать!",
        body=f"Привет, {user.email}! Спасибо за регистрацию в нашем блоге."
    )

    return db_user
