from datetime import datetime

from app.utils.datetime import utcnow


def validate_card_exp_date(exp: str):
    try:
        parsed = datetime.strptime(exp, "%m/%Y")
    except ValueError as error:
        msg = f'Expiration date "{exp}" does not match format "MM/YYYY" or is not a valid date'
        raise ValueError(msg) from error

    today = utcnow().date()

    if parsed.date() <= today:
        raise ValueError(f'The expiration date "{exp}" is already expired')

    return exp
