from pydantic import BaseModel, ConfigDict


class Entity(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_max_length=300,
    )
