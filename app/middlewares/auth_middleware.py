from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.business.user import find_user_by_name

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate(token: Annotated[str, Depends(_oauth2_scheme)]):
    user = find_user_by_name(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
