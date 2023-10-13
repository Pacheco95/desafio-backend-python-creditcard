from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    db_uri: str
    jwt_secret: str
