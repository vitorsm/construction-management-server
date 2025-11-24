from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.expense import Expense, ExpenseType
from src.entities.generic_entity import GenericEntity
from src.service.expense_service import ExpenseService
from src.service.generic_service import GenericService
from src.service.item_service import ItemService
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.expense_repository import ExpenseRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from tests.mocks import expense_mock, item_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestExpenseService(GenericServiceTest):
    def setUp(self):
        self.authentication_repository = Mock(spec_set=AuthenticationRepository)
        self.workspace_repository = Mock(spec_set=WorkspaceRepository)
        self.expense_repository = Mock(spec_set=ExpenseRepository)
        self.item_service = Mock(spec_set=ItemService)

        self.service = ExpenseService(self.authentication_repository, self.workspace_repository,
                                      self.expense_repository, self.item_service)

        self.valid_item = item_mock.get_valid_item()
        self.valid_expense = expense_mock.get_valid_expense()
        self.valid_expense.items = [self.valid_item]

        self.item_service.find_by_id.return_value = self.valid_item

        super().setUp()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.expense_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def get_workspace_repository(self) -> Mock:
        return self.workspace_repository

    def get_valid_entity(self) -> GenericEntity:
        return self.valid_expense

    def get_changed_entity(self) -> GenericEntity:
        expense = Expense(**self.valid_expense.__dict__)
        expense.expense_type = ExpenseType.SERVICE
        expense.name = "Service 1"

        return expense

    def get_different_entity(self) -> GenericEntity:
        return expense_mock.get_valid_expense()

    def test_create_expense_with_invalid_item(self):
        # given
        entity = self.valid_entity
        self.item_service.find_by_id.side_effect = EntityNotFoundException("Item", "id")

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().create(entity)

        self.assertIn("items", str(ex.exception))

    def test_update_expense_with_invalid_item(self):
        # given
        entity = self.valid_entity
        self.item_service.find_by_id.side_effect = EntityNotFoundException("Item", "id")

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(entity)

        self.assertIn("items", str(ex.exception))

    def test_create_expense_without_permission_to_item(self):
        # given
        entity = self.valid_entity
        self.item_service.find_by_id.side_effect = PermissionException(self.default_workspace, self.current_user)

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().create(entity)

        self.assertIn("items", str(ex.exception))

    def test_update_expense_without_permission_to_item(self):
        # given
        entity = self.valid_entity
        self.item_service.find_by_id.side_effect = PermissionException(self.default_workspace, self.current_user)

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(entity)

        self.assertIn("items", str(ex.exception))
