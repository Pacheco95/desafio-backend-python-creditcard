from fastapi.routing import APIRouter
from starlette import status

from app.business.card import create_card
from app.domain.card import Card, CreateCard
from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/card", tags=[RouterTags.CARD])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Card)
def create_card_endpoint(card: CreateCard):
    return create_card(card)
