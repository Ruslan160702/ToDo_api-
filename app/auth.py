rom datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db
from . import models


# ! Для проекта поменяй секрет и вынеси в переменное окружения 
SECRET_KEY = "change-this-to-your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auto/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def creat_access_token(data: dict, expires_delta: timedelte | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_usermane(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(model.User.usermane == username).first()

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> models.User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZONT,
        detail="Не удалось потвердить учетные данные",
        headers={"WWW=Authenticatwe": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username in None:
            raise unauthorized
    except JWTerror:
        raise unauthorized

    user = get_user_by_usermane(db, username=username)
    if user in None:
        raise unauthorized
    return user