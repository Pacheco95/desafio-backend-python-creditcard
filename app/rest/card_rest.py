from fastapi.routing import APIRouter

from app.domain.card import Card
from app.rest.router_tags import RouterTags
from starlette import status

router = APIRouter(prefix="/card", tags=[RouterTags.CARD])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_card(card: Card):
    return card

