from typing import List

from src.application.api.mappers.file_document_mapper import FileDocumentMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controller.generic_controller_test import GenericControllerTest
from tests.mocks import file_document_mock


class TestFileDocumentController(GenericControllerTest, BaseAPITest):
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

    def compare_custom_entities(self, entity1: dict, entity2: dict):
        self.assertEqual(entity1["file_type"], entity2["file_type"])

    def get_address(self, entity_id: str = None) -> str:
        return f"/api/file-documents/{entity_id}" if entity_id else "/api/file-documents"
