from typing import List

from src.application.api.mappers.project_mapper import ProjectMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controller.generic_controller_test import GenericControllerTest
from tests.mocks import project_mock


class TestProjectController(GenericControllerTest, BaseAPITest):

    def get_valid_entity(self) -> dict:
        project = project_mock.get_default_project()
        dto = ProjectMapper.to_dto(project)
        self._remove_tracking_fields_from_dto(dto)
        return dto

    def get_changed_entity(self) -> dict:
        dto = self.get_valid_entity()
        dto["name"] = "Updated Project Name"
        dto["budget"] = 115
        return dto

    def get_invalid_entity(self) -> List[dict]:
        entity = self.get_valid_entity()
        entity["name"] = ""
        entity["budget"] = -10
        return [entity]

    def compare_custom_entities(self, entity1: dict, entity2: dict):
        self.assertEqual(entity1["budget"], entity2["budget"])

    def get_address(self, entity_id: str = None) -> str:
        address = "/api/projects"
        if entity_id:
            address += f"/{entity_id}"
        return address
