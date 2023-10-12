from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import Response

from app.business.card import create_card, find_card_by_id
from app.domain.card import Card, CreateCard
from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/card", tags=[RouterTags.CARD])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Card)
def create_card_endpoint(card: CreateCard):
    return create_card(card)


@router.get("/{card_id}")
def create_card_endpoint(card_id: str, response: Response) -> Card | None:
    found = find_card_by_id(card_id)
    response.status_code = status.HTTP_200_OK if found else status.HTTP_404_NOT_FOUND
    return found if found else None
