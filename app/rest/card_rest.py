from typing import Annotated

from fastapi import Query, Depends
from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import Response

from app.business.card import create_card, find_card_by_id, find_all_cards
from app.business.security import get_current_user
from app.domain.card import Card, CreateCard
from app.domain.user import User
from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/cards", tags=[RouterTags.CARD], dependencies=[Depends(get_current_user)])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Card)
def create_card_endpoint(card: CreateCard, user: Annotated[User, Depends(get_current_user)]):
    return create_card(card, creator=user)


@router.get("/{card_id}")
def find_card_by_id_endpoint(card_id: str, response: Response) -> Card | None:
    found = find_card_by_id(card_id)
    response.status_code = status.HTTP_200_OK if found else status.HTTP_404_NOT_FOUND
    return found if found else None


@router.get("/", response_model=list[Card])
def find_all_cards_by_id_endpoint(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=1000)] = 10
):
    found = find_all_cards(skip, limit)
    return found
