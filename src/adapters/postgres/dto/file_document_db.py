from sqlalchemy import Column, String

from src.adapters.postgres.dto import Base
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.file_document import FileDocument, FileType
from src.utils import enum_utils


class FileDocumentDB(GenericEntityDB, Base[FileDocument]):
    __tablename__ = "file_document"

    file_type = Column(String(100), nullable=False)

    def __init__(self, file_document: FileDocument):
        super().__init__(file_document)
        self.update_attributes(file_document)

    def update_attributes(self, file_document: FileDocument):
        super().update_attributes(file_document)
        self.file_type = file_document.file_type.name

    def to_entity(self) -> FileDocument:
        file_document = object.__new__(FileDocument)
        file_document.file_type = enum_utils.instantiate_enum_from_str_name(FileType, self.file_type)
        self.fill_entity(file_document)
        return file_document
