from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status

from app.business.security import check_password
from app.business.user import find_user_by_name
from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/token", tags=[RouterTags.TOKEN])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = find_user_by_name(form_data.username)

    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user:
        raise unauthorized_exception

    if not check_password(form_data.password, user.encrypted_password):
        raise unauthorized_exception

    return Token(access_token=user.username)
