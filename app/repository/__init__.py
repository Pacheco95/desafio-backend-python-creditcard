from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property, cache
from typing import TypeVar, Generic, Type, Any

from bson import ObjectId
from pydantic import Field

from app.config.app_config import AppConfig
from app.domain.entity import Entity
from app.utils.datetime import utcnow


@cache
def get_database():
    import pymongo

    app_config = AppConfig()
    database = pymongo.MongoClient(app_config.db_uri).get_default_database()

    return database


class Storable(ABC, Entity):
    id: str = Field("", examples=["65279820aa60482099e67693"])

    @classmethod
    @abstractmethod
    def get_collection(cls) -> str:
        ...  # pragma: no cover


class Auditable(Entity):
    created_at: datetime = Field(default_factory=utcnow)
    created_by: str


T = TypeVar('T', bound=Storable)


class Repository(Generic[T]):
    def __init__(self, model: Type[T]) -> None:
        self._model_type = model

    @cached_property
    def _collection(self):
        database = get_database()
        collection = self._model_type.get_collection()
        return database[collection]

    def insert(self, data: T):
        serialized = data.model_dump(exclude={"id"})
        result = self._collection.insert_one(serialized.copy())
        new_document = {**serialized, "id": str(result.inserted_id)}
        return self._model_type.model_validate(new_document)

    def find_one(self, query: dict[str, Any]) -> T | None:
        document = self._collection.find_one(query)
        deserialized = self._from_db(document) if document else None
        return deserialized

    def find_by_id(self, doc_id: str):
        found = self.find_one({"_id": ObjectId(doc_id)})
        return found

    def find_many(self, skip: int, limit: int):
        documents = self._collection.find({}).skip(skip).limit(limit)
        deserialized_documents = list(map(self._from_db, documents))
        return deserialized_documents

    def _from_db(self, document: dict[str, Any]):
        document["id"] = str(document.pop("_id"))
        deserialized = self._model_type.model_validate(document)
        return deserialized
