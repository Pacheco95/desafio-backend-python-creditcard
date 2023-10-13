from pymongo import IndexModel

from base_migration import BaseMigration

_COLLECTION = "cards"


class Migration(BaseMigration):

    def upgrade(self):
        super().upgrade()
        self.create_collection_if_not_exists(_COLLECTION)
        indexes = [
            IndexModel(["holder", "exp_date", "cvv"], unique=True),
            IndexModel("created_at"),
            IndexModel("created_by"),
        ]
        self.db[_COLLECTION].create_indexes(indexes)

    def downgrade(self):
        super().downgrade()
        self.drop_collection_if_exists(_COLLECTION)
