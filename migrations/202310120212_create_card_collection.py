from pymongo import ASCENDING

from base_migration import BaseMigration

_COLLECTION = "card"


class Migration(BaseMigration):

    def upgrade(self):
        self.create_collection_if_not_exists(_COLLECTION)
        fields = [("holder", ASCENDING), ("number", ASCENDING), ("cvv", ASCENDING)]
        self.create_index_if_not_exists(_COLLECTION, fields, unique=True)

    def downgrade(self):
        self.drop_collection_if_exists(_COLLECTION)
