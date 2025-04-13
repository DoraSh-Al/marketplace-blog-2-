from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserOut
from src.tasks import send_email
from src.utils.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": user.email})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=1800)
    send_email.delay(
        to_email=user.email,
        subject="Добро пожаловать!",
        body=f"Привет, {user.email}! Спасибо за регистрацию."
    )
    return new_user

@router.post("/login")
def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == login_data.email).first()
    if not db_user or not verify_password(login_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=1800)
    return {"msg": "Login successful"}
