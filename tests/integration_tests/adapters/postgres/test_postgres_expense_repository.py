from src.adapters.postgres.postgres_expense_repository import PostgresExpenseRepository
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.expense import Expense, ExpenseType, ExpenseClass
from src.entities.generic_entity import GenericEntity
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_integration_test import BaseIntegrationTest
from tests.mocks import expense_mock, SECOND_DEFAULT_ID


class TestPostgresExpenseRepository(GenericEntityRepositoryTest, BaseIntegrationTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresExpenseRepository(self.db_engine)

    def get_repository(self) -> PostgresExpenseRepository:
        return self.repository

    def get_first_entity(self) -> Expense:
        return expense_mock.get_default_expense()

    def get_second_entity(self) -> Expense:
        entity = self.get_first_entity()
        entity.id = SECOND_DEFAULT_ID
        entity.name = "Expense 2"
        entity.expense_type = ExpenseType.SERVICE
        entity.expense_class = ExpenseClass.PLANNING
        entity.value = 200.0
        entity.notes = None
        entity.items = []
        return entity

    def get_changed_entity(self) -> Expense:
        entity = self.get_first_entity()
        entity.name = "changed name"
        entity.expense_type = ExpenseType.DOCUMENT
        entity.expense_class = ExpenseClass.PLANNING
        entity.value = 150.0
        entity.notes = "new notes"
        return entity

    def assert_entity_equal(self, entity1: Expense, entity2: Expense):
        self.assertEqual(entity1.expense_type, entity2.expense_type)
        self.assertEqual(entity1.expense_class, entity2.expense_class)
        self.assertEqual(entity1.value, entity2.value)
        self.assertEqual(entity1.notes, entity2.notes)
