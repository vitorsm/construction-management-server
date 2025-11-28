from typing import List
from uuid import uuid4

from src.application.api.mappers.project_mapper import ProjectMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controller.generic_controller_test import GenericControllerTest
from tests.mocks import project_mock, FIRST_DEFAULT_ID, SECOND_DEFAULT_ID


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

    def test_get_tasks_by_project(self):
        # given
        project_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(project_id) + "/tasks"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        tasks_response = response.json
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual(2, len(tasks_response))
        self.assertEqual(str(FIRST_DEFAULT_ID), tasks_response[0]["id"])
        self.assertEqual(str(SECOND_DEFAULT_ID), tasks_response[1]["id"])
        self.assertEqual("Task 1", tasks_response[0]["name"])
        self.assertEqual("Task 2", tasks_response[1]["name"])

    def test_get_tasks_by_project_not_found(self):
        # given
        project_id = str(uuid4())
        address = self.get_address(project_id) + "/tasks"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(404, response.status_code, response.text)

    def test_get_tasks_by_project_empty_list(self):
        # given
        project_id = str(SECOND_DEFAULT_ID)
        address = self.get_address(project_id) + "/tasks"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        tasks_response = response.json
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual(0, len(tasks_response))

    def test_get_tasks_by_project_without_permission(self):
        # given
        project_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(project_id) + "/tasks"

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_permission=False))

        # then
        self.assertEqual(403, response.status_code, response.text)
