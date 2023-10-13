from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.business.security import Token, authenticate_user, create_access_token
from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/token", tags=[RouterTags.TOKEN])


@router.post("/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.username})

    return Token(access_token=access_token)
