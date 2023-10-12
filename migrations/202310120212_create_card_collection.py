from pymongo import ASCENDING

from base_migration import BaseMigration

_COLLECTION = "card"


class Migration(BaseMigration):

    def upgrade(self):
        super().upgrade()
        self.create_collection_if_not_exists(_COLLECTION)
        fields = [("holder", ASCENDING), ("exp_date", ASCENDING), ("cvv", ASCENDING)]
        self.db[_COLLECTION].create_index(fields, unique=True)

    def downgrade(self):
        super().downgrade()
        self.drop_collection_if_exists(_COLLECTION)
