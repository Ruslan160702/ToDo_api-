from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..auth import get_password_hash, verify_password, create_access_token, get_user_by_username

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreat, db: Session - Depends(get_db)):
    existing = get_user_by_usermane(db, username=user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    user = model.User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(from_data; OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_usermane(db, username=from_data.username)
    if not user or not verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    
    token = creat_access_token(data={"sub": user.username, "uid": user.id})
    return {"access_token": token, "token_type": "bearer"}
