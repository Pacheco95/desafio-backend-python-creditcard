from pydantic import StringConstraints, AfterValidator
from typing_extensions import Annotated

from app.business.validators import validate_card_exp_date
from app.domain.entity import Entity

ExpirationDate = Annotated[
    str,
    StringConstraints(to_upper=True, pattern=r"\d{2}/\d{4}"),
    AfterValidator(validate_card_exp_date)
]


class Card(Entity):
    exp_date: ExpirationDate
