from enum import Enum


class RouterTags(str, Enum):
    CARD = "Card"
    HEALTH = "Health"
    TOKEN = "Token"
    USERS = "Users"
