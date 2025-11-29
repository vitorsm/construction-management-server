from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.file_document_db import FileDocumentDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.file_document import FileDocument
from src.service.ports.file_document_repository import FileDocumentRepository


class PostgresFileDocumentRepository(PostgresGenericRepository[FileDocument, FileDocumentDB], FileDocumentRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
