from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from app.config.app_config import AppConfig
from app.utils.datetime import utcnow

SECRET_KEY = AppConfig().jwt_secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def check_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def encrypt(s: str):
    return pwd_context.hash(s)


def create_access_token(data: dict, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    now = utcnow()
    expire = now + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    from app.business.user import find_user_by_name

    user = find_user_by_name(username)

    if not user:
        return None

    if not check_password(password, user.encrypted_password):
        return None

    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    from app.business.user import find_user_by_name

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError as error:
        raise credentials_exception from error

    user = find_user_by_name(username)

    if user is None:
        raise credentials_exception

    return user
