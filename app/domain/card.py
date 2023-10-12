from pydantic import StringConstraints, AfterValidator, Field
from typing_extensions import Annotated

from app.business.validators import validate_card_exp_date
from app.domain.entity import Entity

ExpirationDate = Annotated[
    str,
    StringConstraints(pattern=r"\d{2}/\d{4}"),
    AfterValidator(validate_card_exp_date)
]


class Card(Entity):
    exp_date: ExpirationDate
    holder: Annotated[str, StringConstraints(min_length=2, to_upper=True)]
    cvv: int = Field(ge=100, le=9999)
