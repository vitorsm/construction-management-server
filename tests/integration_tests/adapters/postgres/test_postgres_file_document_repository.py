import io

from src.adapters.postgres.postgres_file_document_repository import PostgresFileDocumentRepository
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.file_document import FileDocument
from src.entities.generic_entity import GenericEntity
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.mocks import file_document_mock, SECOND_DEFAULT_ID


class TestPostgresFileDocumentRepository(GenericEntityRepositoryTest, BaseSQLAlchemyTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresFileDocumentRepository(self.db_instance)

    def get_repository(self) -> PostgresGenericRepository:
        return self.repository

    def get_first_entity(self) -> GenericEntity:
        document = file_document_mock.get_default_file_document()
        document.file = b"file content"
        return document

    def get_second_entity(self) -> GenericEntity:
        document = self.get_first_entity()
        document.id = SECOND_DEFAULT_ID
        document.name = "File 2"
        return document

    def get_changed_entity(self) -> GenericEntity:
        document = self.get_first_entity()
        document.name = "new name"
        return document

    def assert_entity_equal(self, entity1: FileDocument, entity2: FileDocument):
        self.assertEqual(entity1.file_type, entity2.file_type)
