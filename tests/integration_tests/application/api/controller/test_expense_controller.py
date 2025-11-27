import uuid
from typing import List

from src.application.api.mappers.expense_mapper import ExpenseMapper
from src.entities.expense import ExpenseType, ExpenseClass
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controller.generic_controller_test import GenericControllerTest
from tests.mocks import expense_mock


class TestExpenseController(BaseAPITest, GenericControllerTest):
    def get_valid_entity(self) -> dict:
        expense = expense_mock.get_default_expense()
        dto = ExpenseMapper.to_dto(expense)
        self._remove_tracking_fields_from_dto(dto)
        return dto

    def get_changed_entity(self) -> dict:
        dto = self.get_valid_entity()
        dto["name"] = "Updated Expense Name"
        dto["value"] = 2500.75
        dto["expense_type"] = ExpenseType.TRANSPORT.name
        dto["expense_class"] = ExpenseClass.PLANNING.name
        dto["items"] = []

        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_valid_entity()
        dto1["name"] = ""

        dto2 = self.get_valid_entity()
        dto2["value"] = -10

        dto3 = self.get_valid_entity()
        dto3["value"] = "10"

        dto4 = self.get_valid_entity()
        dto4["expense_type"] = "INVALID_TYPE"

        dto5 = self.get_valid_entity()
        dto5["expense_class"] = "INVALID_CLASS"

        dto6 = self.get_valid_entity()
        dto6["items"] = [{"id": str(uuid.uuid4())}]

        return [dto1, dto2, dto3, dto4, dto5]

    def compare_custom_entities(self, entity1: dict, entity2: dict):
        self.assertEqual(entity1["expense_type"], entity2["expense_type"])
        self.assertEqual(entity1["expense_class"], entity2["expense_class"])
        self.assertEqual(entity1["value"], entity2["value"])
        self.assertEqual(entity1["items"], entity2["items"])

    def get_address(self, entity_id: str = None) -> str:
        return f"/api/expenses/{entity_id}" if entity_id else "/api/expenses"
