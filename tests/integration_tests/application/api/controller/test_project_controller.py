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
        self.assertEqual(1, len(tasks_response))
        self.assertEqual(str(FIRST_DEFAULT_ID), tasks_response[0]["id"])
        self.assertEqual(1, len(tasks_response[0]["children"]))
        self.assertEqual("Task 1", tasks_response[0]["name"])
        self.assertEqual(str(SECOND_DEFAULT_ID), tasks_response[0]["children"][0]["id"])
        self.assertEqual("Task 2", tasks_response[0]["children"][0]["name"])

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

    def test_get_feed_items(self):
        # given
        project_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(project_id) + "/feed"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        feed_items = response.json
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual(2, len(feed_items))
        self.assertEqual("Started working on the task", feed_items[0]["notes"])
        self.assertEqual(10, feed_items[0]["progress"])
        self.assertEqual("IN_PROGRESS", feed_items[0]["status"])
        self.assertEqual(str(FIRST_DEFAULT_ID), feed_items[0]["created_by"]["id"])
        self.assertEqual("User 1", feed_items[0]["created_by"]["name"])
        self.assertEqual("user1", feed_items[0]["created_by"]["login"])
        self.assertIsNone(feed_items[0]["created_by"]["password"])
        self.assertEqual("Task 1", feed_items[0]["source"]["name"])
        self.assertEqual("2025-11-02T10:31:00", feed_items[0]["source"]["planned_start_date"])
        self.assertEqual("2025-11-03T10:31:00", feed_items[0]["source"]["planned_end_date"])
        self.assertEqual("2025-11-04T10:31:00", feed_items[0]["source"]["actual_start_date"])
        self.assertEqual("2025-11-05T10:31:00", feed_items[0]["source"]["actual_end_date"])

    def test_get_feed_items_not_found_project(self):
        # given
        project_id = str(uuid4())
        address = self.get_address(project_id) + "/feed"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(404, response.status_code)

    def test_get_feed_items_without_permission(self):
        # given
        project_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(project_id) + "/feed"

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_permission=False))

        # then
        self.assertEqual(403, response.status_code)

    def test_get_expenses_by_project(self):
        # given
        project_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(project_id) + "/expenses"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        expense_response = response.json
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual(2, len(expense_response))
        self.assertEqual(str(FIRST_DEFAULT_ID), expense_response[0]["id"])
        self.assertEqual(str(SECOND_DEFAULT_ID), expense_response[1]["id"])
        self.assertEqual("Expense 1", expense_response[0]["name"])
        self.assertEqual("Expense 2", expense_response[1]["name"])

    def test_get_expenses_by_project_not_found(self):
        # given
        project_id = str(uuid4())
        address = self.get_address(project_id) + "/expenses"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(404, response.status_code, response.text)

    def test_get_expenses_by_project_without_permission(self):
        # given
        project_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(project_id) + "/expenses"

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_permission=False))

        # then
        self.assertEqual(403, response.status_code, response.text)

