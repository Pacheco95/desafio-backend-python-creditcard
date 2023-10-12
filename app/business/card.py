from uuid import uuid4

from creditcard import CreditCard

from app.domain.card import CreateCard, Card


def create_card(card_dto: CreateCard):
    brand = CreditCard(card_dto.number).get_brand()
    return Card(id=str(uuid4()), brand=brand, **card_dto.model_dump())
