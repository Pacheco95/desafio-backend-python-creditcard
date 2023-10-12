from pathlib import Path

import pytest
from mongodb_migrations.cli import MigrationManager
from mongodb_migrations.config import Execution

from app.config.app_config import AppConfig
from app.repository import get_database


@pytest.fixture(scope="session")
def migration_manager():
    app_config = AppConfig()
    migrations_directory = (Path(__file__).parent.parent / "migrations").resolve()

    manager = MigrationManager()
    manager.config.mongo_url = app_config.db_uri
    manager.config.mongo_migrations_path = str(migrations_directory)

    return manager


@pytest.fixture(autouse=True, scope="session")
def run_migrations(migration_manager):
    migration_manager.config.execution = Execution.DOWNGRADE
    migration_manager.run()

    migration_manager.config.execution = Execution.MIGRATE
    migration_manager.run()


@pytest.fixture(autouse=True)
def clear_collections(migration_manager):
    db = get_database()

    collections = [
        collection
        for collection in db.list_collection_names()
        if collection != migration_manager.config.metastore
    ]

    for collection in collections:
        db[collection].delete_many({})
