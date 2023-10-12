from datetime import datetime


def validate_card_exp_date(exp: str):
    try:
        datetime.strptime(exp, "%m/%Y")
        return exp
    except ValueError as error:
        msg = f'Expiration date "{exp}" does not match format "MM/YYYY" or is not a valid date'
        raise ValueError(msg) from error
