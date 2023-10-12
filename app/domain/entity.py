from pydantic import BaseModel, ConfigDict


class Entity(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_max_length=300,
    )

    @classmethod
    def f(cls, field_name: str):
        """Returns the given field name as if serialized"""
        field = cls.model_fields[field_name]
        alias = field.serialization_alias
        serialized_name = alias if alias else field_name
        return serialized_name
