from typing import Literal, Sequence

import mongodb_migrations.base
from pymongo import IndexModel


class BaseMigration(mongodb_migrations.base.BaseMigration):
    def upgrade(self):
        ...

    def downgrade(self):
        ...

    def create_collection_if_not_exists(self, collection: str):
        if collection in self.db.list_collection_names():
            return

        self.db.create_collection(collection)

    def drop_collection_if_exists(self, collection: str):
        if collection in self.db.list_collection_names():
            self.db.drop_collection(collection)

    def create_indexes_if_not_exists(
        self, collection: str, indexes: Sequence[IndexModel]
    ):
        self._ensure_collection_exists(collection)
        self.db[collection].create_indexes(indexes)

    def create_index_if_not_exists(
        self,
        collection: str,
        fields: Sequence[tuple[str, Literal[1, -1]]],
        *,
        name: str = None,
        unique=False,
    ):
        kwargs = {"unique": unique}

        if name is not None:
            kwargs["name"] = name

        self._ensure_collection_exists(collection)
        self.db[collection].create_index(fields, **kwargs)

    def drop_index_if_exists(
        self,
        collection: str,
        index: tuple[str, Literal[1, -1]] | str,
    ):
        self._ensure_collection_exists(collection)
        self.db[collection].drop_index(index)

    def _ensure_collection_exists(self, collection: str):
        if collection not in self.db.list_collection_names():
            raise ValueError(f"Collection not found{collection}`")
