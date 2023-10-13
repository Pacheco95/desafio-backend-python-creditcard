from app.domain.entity import Entity
from app.repository import Storable


class BaseUser(Entity):
    username: str


class CreateUser(BaseUser):
    password: str


class User(BaseUser, Storable):
    encrypted_password: str

    @classmethod
    def get_collection(cls) -> str:
        return "users"
