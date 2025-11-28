from typing import List
from uuid import uuid4

from src.application.api.mappers.task_history_mapper import TaskHistoryMapper
from src.application.api.mappers.task_mapper import TaskMapper
from src.entities.task import TaskStatus
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controller.generic_controller_test import GenericControllerTest
from tests.mocks import task_mock, FIRST_DEFAULT_ID, user_mock, SECOND_DEFAULT_ID


class TestTaskController(GenericControllerTest, BaseAPITest):

    def get_valid_entity(self) -> dict:
        task = task_mock.get_default_task()
        dto = TaskMapper.to_dto(task)
        self._remove_tracking_fields_from_dto(dto)
        return dto

    def get_changed_entity(self) -> dict:
        dto = self.get_valid_entity()

        dto["name"] = "Updated Task Name"
        dto["progress"] = 75
        dto["planned_start_date"] = "2024-07-01T09:00:00Z"
        dto["planned_end_date"] = "2024-07-15T17:00:00Z"
        dto["status"] = "IN_PROGRESS"
        dto["actual_start_date"] = "2024-07-02T10:00:00Z"
        dto["actual_end_date"] = None

        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_valid_entity()
        dto1["progress"] = "1"

        dto2 = self.get_valid_entity()
        dto2["name"] = ""

        dto3 = self.get_valid_entity()
        dto3["status"] = "INVALID_STATUS"

        return [dto1, dto2, dto3]

    def compare_custom_entities(self, entity1: dict, entity2: dict):
        self.assertEqual(entity1["progress"], entity2["progress"])
        self.assertEqual(entity1["planned_start_date"], entity2["planned_start_date"])
        self.assertEqual(entity1["planned_end_date"], entity2["planned_end_date"])
        self.assertEqual(entity1["actual_start_date"], entity2["actual_start_date"])
        self.assertEqual(entity1["actual_end_date"], entity2["actual_end_date"])
        self.assertEqual(entity1["status"], entity2["status"])
        self.assertEqual(entity1["project"]["id"], entity2["project"]["id"])

    def get_address(self, entity_id: str = None) -> str:
        return f"/api/tasks/{entity_id}" if entity_id else "/api/tasks"

    def test_create_task_history(self):
        # given
        task_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(task_id) + "/history"
        task_history = task_mock.get_task_history()
        task_history.status = TaskStatus.DONE
        task_history.created_by = user_mock.get_default_user()
        dto = TaskHistoryMapper.to_dto(task_history)

        # when
        response = self.client.post(address, json=dto, headers=self.get_default_headers())

        # then
        response_data = response.json
        self.assertEqual(201, response.status_code, response.text)
        self.assertEqual(dto["status"], response_data["status"])
        self.assertEqual(dto["progress"], response_data["progress"])
        self.assertEqual(str(FIRST_DEFAULT_ID), response_data["created_by"]["id"])

        response = self.client.get(self.get_address(task_id), headers=self.get_default_headers())
        self.assertEqual(task_history.status.name, response.json["status"])

    def test_create_task_history_without_permission(self):
        # given
        task_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(task_id) + "/history"
        task_history = task_mock.get_task_history()
        task_history.created_by = user_mock.get_default_user()
        dto = TaskHistoryMapper.to_dto(task_history)

        # when
        response = self.client.post(address, json=dto, headers=self.get_default_headers(with_permission=False))

        # then
        response_data = response.json
        self.assertEqual(403, response.status_code, response.text)
        self.assertIn(str(SECOND_DEFAULT_ID), response_data["details"])

    def test_create_task_history_not_found(self):
        # given
        task_id = str(uuid4())
        address = self.get_address(task_id) + "/history"
        task_history = task_mock.get_task_history()
        task_history.created_by = user_mock.get_default_user()
        dto = TaskHistoryMapper.to_dto(task_history)

        # when
        response = self.client.post(address, json=dto, headers=self.get_default_headers(with_permission=False))

        # then
        response_data = response.json
        self.assertEqual(404, response.status_code, response.text)
