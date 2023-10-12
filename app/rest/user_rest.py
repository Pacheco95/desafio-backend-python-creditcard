from fastapi.routing import APIRouter
from starlette import status

from app.business.user import create_user
from app.domain.user import CreateUser, User
from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/users", tags=[RouterTags.USERS])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: CreateUser) -> User:
    created = create_user(user)
    return created
