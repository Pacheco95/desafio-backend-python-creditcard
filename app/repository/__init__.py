from abc import ABC, abstractmethod
from functools import cached_property
from typing import TypeVar, Generic, Type

from bson import ObjectId

from app.domain.entity import Entity


class Storable(ABC, Entity):
    id: str = ""

    @classmethod
    @abstractmethod
    def get_collection(cls) -> str:
        ...


T = TypeVar('T', bound=Storable)


class Repository(Generic[T]):
    def __init__(self, model: Type[T]) -> None:
        self._model_type = model

    @cached_property
    def _collection(self):
        import pymongo
        import os

        db_uri = os.getenv("db_uri")
        database = pymongo.MongoClient(db_uri).get_default_database()
        collection = self._model_type.get_collection()
        return database[collection]

    def insert(self, data: T):
        serialized = data.model_dump(exclude={"id"})
        result = self._collection.insert_one(serialized.copy())
        new_document = {**serialized, "id": str(result.inserted_id)}
        return self._model_type.model_validate(new_document)

    def find_by_id(self, doc_id: str):
        document = self._collection.find_one({"_id": ObjectId(doc_id)})

        if not document:
            return None

        document["id"] = str(document.pop("_id"))
        deserialized = self._model_type.model_validate(document)
        return deserialized
