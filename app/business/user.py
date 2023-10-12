from app.business.security import encrypt
from app.domain.user import CreateUser, User
from app.repository import Repository

_repo = Repository[User](User)


def create_user(user_dto: CreateUser):
    user = User(**user_dto.model_dump(), encrypted_password=encrypt(user_dto.password))
    stored = _repo.insert(user)
    return stored


def find_user_by_name(username: str):
    query = {User.f("username"): username}
    found = _repo.find_one(query)
    return found
