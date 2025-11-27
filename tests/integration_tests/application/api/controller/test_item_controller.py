from typing import List

from src.application.api.mappers.item_mapper import ItemMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controller.generic_controller_test import GenericControllerTest
from tests.mocks import item_mock


class TestItemController(BaseAPITest, GenericControllerTest):
    def get_valid_entity(self) -> dict:
        item = item_mock.get_default_item()
        item_dto = ItemMapper.to_dto(item)
        self._remove_tracking_fields_from_dto(item_dto)
        return item_dto

    def get_changed_entity(self) -> dict:
        dto = self.get_valid_entity()
        dto["name"] = "Updated Item Name"
        dto["unit_of_measurement"] = "packages"
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto = self.get_valid_entity()
        dto["name"] = ""
        del dto["unit_of_measurement"]
        return [dto]

    def compare_custom_entities(self, entity1: dict, entity2: dict):
        self.assertEqual(entity1["unit_of_measurement"], entity2["unit_of_measurement"])

    def get_address(self, entity_id: str = None) -> str:
        return f"/api/items/{entity_id}" if entity_id else "/api/items"