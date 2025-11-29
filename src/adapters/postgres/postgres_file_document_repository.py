import os
from typing import Optional
from uuid import UUID

from src import config
from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.file_document_db import FileDocumentDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository, Entity
from src.entities.file_document import FileDocument, FileType
from src.service.ports.file_document_repository import FileDocumentRepository


FILE_REPOSITORY_DIR = config.FILE_REPOSITORY


class PostgresFileDocumentRepository(PostgresGenericRepository[FileDocument, FileDocumentDB], FileDocumentRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def create(self, file_document: FileDocument):
        entity_db = FileDocumentDB(file_document)
        session = self.get_session()
        session.add(entity_db)

        self.__persist_file(file_document)

        session.commit()

    def find_by_id(self, file_id: UUID, fill_file: bool = False) -> Optional[FileDocument]:
        file_document = super().find_by_id(file_id)

        if not file_document:
            return file_document

        self.__load_file(file_document)

        return file_document

    def __load_file(self, file_document: FileDocument):
        file_path = self.__get_file_path(file_document)
        if not os.path.exists(file_path):
            return

        with open(file_path, "rb") as f:
            file_document.file = f.read()

    def __persist_file(self, file_document: FileDocument):
        file_path = self.__get_file_path(file_document)

        directory_path = os.path.dirname(file_path)
        os.makedirs(directory_path, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(file_document.file)

    @staticmethod
    def __get_file_path(file_document: FileDocument) -> str:
        return os.path.join(FILE_REPOSITORY_DIR, str(file_document.workspace.id), file_document.file_type.name,
                            str(file_document.id))
