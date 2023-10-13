from base_migration import BaseMigration

_COLLECTION = "users"


class Migration(BaseMigration):
    def upgrade(self):
        super().upgrade()
        self.create_collection_if_not_exists(_COLLECTION)
        self.db[_COLLECTION].create_index("username", unique=True)

    def downgrade(self):
        super().downgrade()
        self.drop_collection_if_exists(_COLLECTION)
