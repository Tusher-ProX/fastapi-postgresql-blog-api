from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from datetime import UTC, datetime, timedelta
import jwt

from core.config import settings
from schemas.users import TokenData
from .database import get_db
from models.users import User

password_hash = PasswordHash.recommended()
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password ,hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes= settings.access_token_expires_minutes)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)

    return  encode_jwt   


def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm])
        id: int | None = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)

    except InvalidTokenError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= f"Could not validate Creditials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.userid == token_data.id).first()

    return user