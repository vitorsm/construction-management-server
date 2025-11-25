from datetime import datetime

from src.adapters.postgres.postgres_item_repository import PostgresItemRepository
from src.entities.item import Item
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_integration_test import BaseIntegrationTest
from tests.mocks import item_mock, SECOND_DEFAULT_ID, user_mock


class TestPostgresItemRepository(GenericEntityRepositoryTest, BaseIntegrationTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresItemRepository(self.db_engine)

    def get_repository(self) -> PostgresItemRepository:
        return self.repository

    def get_first_entity(self) -> Item:
        return item_mock.get_default_item()

    def get_second_entity(self) -> Item:
        entity = self.get_first_entity()
        entity.id = SECOND_DEFAULT_ID
        entity.name = "Item 2"
        entity.unit_of_measurement = "packages"

        return entity

    def get_changed_entity(self) -> Item:
        user = user_mock.get_default_user()
        user.id = SECOND_DEFAULT_ID

        entity = self.get_first_entity()
        entity.name = "changed name"
        entity.unit_of_measurement = "unit"
        entity.updated_at = datetime.now()
        entity.updated_by = user

        return entity

    def assert_entity_equal(self, entity1: Item, entity2: Item):
        self.assertEqual(entity1.unit_of_measurement, entity2.unit_of_measurement)
