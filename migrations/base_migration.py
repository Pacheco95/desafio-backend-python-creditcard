import mongodb_migrations.base


class BaseMigration(mongodb_migrations.base.BaseMigration):
    def upgrade(self):
        ...

    def downgrade(self):
        ...

    def create_collection_if_not_exists(self, collection: str):
        if collection in self.db.list_collection_names():
            return  # pragma: no cover

        self.db.create_collection(collection)

    def drop_collection_if_exists(self, collection: str):
        if collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
