import bcrypt


def encrypt_card_number(number: str):
    encrypted = bcrypt.hashpw(number.encode("utf-8"), bcrypt.gensalt())
    return encrypted.decode("utf-8")
