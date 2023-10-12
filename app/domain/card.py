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
    exp_date: ExpirationDate = Field(..., examples=["01/2028", "12/2033"])
    holder: Annotated[str, StringConstraints(min_length=2, to_upper=True)] = Field(..., examples=["Fulano da Silva"])
    cvv: int = Field(ge=100, le=9999, examples=[100, 9999])
    number: CardNumber = Field(..., examples=["4220036484096326", "4220 0364 8409 6326"])


class Card(CreateCard, Storable):
    @classmethod
    def get_collection(cls) -> str:
        return "card"

    brand: Annotated[str, StringConstraints(to_upper=True)] = Field(..., examples=["VISA", "ELO"])
    number: str = Field(..., examples=["<encrypted>"])

    @field_serializer("number")
    def serialize_card_number(self, number: str):
        return encrypt_card_number(number)
