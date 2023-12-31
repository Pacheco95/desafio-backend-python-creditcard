from creditcard import CreditCard

from app.domain.card import CreateCard, Card
from app.domain.user import User
from app.repository import Repository

_repo = Repository[Card](Card)


def create_card(card_dto: CreateCard, creator: User):
    brand = CreditCard(card_dto.number).get_brand()
    card = Card(brand=brand, **card_dto.model_dump(), created_by=creator.username)
    stored = _repo.insert(card)
    return stored


def find_card_by_id(card_id: str):
    found = _repo.find_by_id(card_id)
    return found


def find_all_cards(skip: int, limit: int):
    found = _repo.find_many(skip, limit)
    return found
