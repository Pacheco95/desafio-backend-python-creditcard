from pydantic import StringConstraints, AfterValidator, Field, field_serializer
from typing_extensions import Annotated

from app.business.security import encrypt_card_number
from app.business.validators import validate_card_exp_date, validate_card_number
from app.domain.entity import Entity
from app.repository import Storable

ExpirationDate = Annotated[
    str,
    StringConstraints(pattern=r"\d{2}/\d{4}"),
    AfterValidator(validate_card_exp_date)
]

CardNumber = Annotated[
    str,
    StringConstraints(pattern=r"\d+"),
    AfterValidator(validate_card_number)
]


class CreateCard(Entity):
    exp_date: ExpirationDate
    holder: Annotated[str, StringConstraints(min_length=2, to_upper=True)]
    cvv: int = Field(ge=100, le=9999)
    number: CardNumber


class Card(CreateCard, Storable):
    @classmethod
    def get_collection(cls) -> str:
        return "card"

    brand: Annotated[str, StringConstraints(to_upper=True)]
    number: str

    @field_serializer("number")
    def serialize_card_number(self, number: str):
        return encrypt_card_number(number)
