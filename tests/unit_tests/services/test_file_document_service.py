from unittest import TestCase
from unittest.mock import Mock

from src.entities.generic_entity import GenericEntity
from src.service.file_document_service import FileDocumentService
from src.service.generic_service import GenericService
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.file_document_repository import FileDocumentRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from tests.mocks import file_document_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestFileDocumentService(GenericServiceTest, TestCase):
    def setUp(self):

        self.authentication_repository = Mock(spec_set=AuthenticationRepository)
        self.workspace_repository = Mock(spec_set=WorkspaceRepository)
        self.file_document_repository = Mock(spec_set=FileDocumentRepository)

        self.service = FileDocumentService(self.authentication_repository, self.workspace_repository,
                                           self.file_document_repository)

        super().setUp()


    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.file_document_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def get_workspace_repository(self) -> Mock:
        return self.workspace_repository

    def get_valid_entity(self) -> GenericEntity:
        return file_document_mock.get_valid_file_document()

    def get_changed_entity(self) -> GenericEntity:
        file = self.get_valid_entity()
        file.name = "new name"
        return file

    def get_different_entity(self) -> GenericEntity:
        return file_document_mock.get_valid_file_document()
