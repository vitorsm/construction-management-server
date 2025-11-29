import io
from typing import List

from src.application.api.mappers.file_document_mapper import FileDocumentMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.mocks import file_document_mock, FIRST_DEFAULT_ID


class TestFileDocumentController(BaseAPITest):

    @staticmethod
    def _remove_tracking_fields_from_dto(dto: dict):
        del dto["created_at"]
        del dto["updated_at"]
        del dto["created_by"]
        del dto["updated_by"]

        if "deleted_at" in dto:
            del dto["deleted_at"]

        if "workspace" in dto:
            dto["workspace"] = {"id": dto["workspace"]["id"]}

    def get_valid_entity(self) -> dict:
        file = file_document_mock.get_default_file_document()
        dto = FileDocumentMapper.to_dto(file)
        self._remove_tracking_fields_from_dto(dto)
        return dto

    def get_changed_entity(self) -> dict:
        dto = self.get_valid_entity()
        dto["name"] = "new name"
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto = self.get_valid_entity()
        dto["name"] = ""
        return [dto]

    def compare_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        if compare_id:
            self.assertEqual(entity1["id"], entity2["id"])

        self.assertEqual(entity1["name"], entity2["name"])
        self.assertEqual(entity1["workspace"]["id"], entity2["workspace"]["id"])

        self.assertEqual(entity1["file_type"], entity2["file_type"])

    def get_address(self, entity_id: str = None) -> str:
        return f"/api/file-documents/{entity_id}" if entity_id else "/api/file-documents"

    def assert_tracking_fields(self, entity: dict):
        self.assertIsNotNone(entity["created_at"])
        self.assertIsNotNone(entity["updated_at"])
        self.assertIsNotNone(entity["created_by"])
        self.assertIsNotNone(entity["updated_by"])

    def test_create_entity(self):
        # given
        address = self.get_address()
        entity = self.get_valid_entity()
        headers = self.get_default_headers()

        data = {
            "file": (io.BytesIO(b"file content"), "photo.png"),
            "workspace_id": str(FIRST_DEFAULT_ID),
            "name": "File 1"
        }


        # when
        response = self.client.post(address, data=data, headers=headers, content_type="multipart/form-data")

        # then
        response_data = response.json
        self.assertEqual(201, response.status_code, response.text)
        self.compare_entities(entity, response_data)
        self.assertIsNotNone(response_data["id"])
        self.assert_tracking_fields(response_data)
