from uuid import uuid4

from src.adapters.postgres.postgres_expense_repository import PostgresExpenseRepository
from src.entities.expense import Expense, ExpenseType, ExpenseClass
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.mocks import expense_mock, SECOND_DEFAULT_ID, FIRST_DEFAULT_ID


class TestPostgresExpenseRepository(GenericEntityRepositoryTest, BaseSQLAlchemyTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresExpenseRepository(self.db_instance)

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
        self.assertEqual(entity1.project, entity2.project)

    def test_find_expenses_by_project(self):
        # given
        project_id = FIRST_DEFAULT_ID

        # when
        expenses = self.repository.find_by_project(project_id)

        # then
        self.assertEqual(2, len(expenses))
        self.assertEqual(FIRST_DEFAULT_ID, expenses[0].id)
        self.assertEqual(SECOND_DEFAULT_ID, expenses[1].id)
        self.assertEqual("Expense 1", expenses[0].name)
        self.assertEqual("Expense 2", expenses[1].name)

    def test_find_expenses_by_project_emtpy(self):
        # given
        project_id = uuid4()

        # when
        expenses = self.repository.find_by_project(project_id)

        # then
        self.assertEqual(0, len(expenses))
