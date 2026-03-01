from typing import Optional

from src.application.api.mappers.generic_entity_mapper import GenericEntityMapper
from src.entities.file_document import FileDocument


class FileDocumentMapper(GenericEntityMapper[FileDocument]):
    @classmethod
    def to_dto(cls, file_document: Optional[FileDocument]) -> Optional[dict]:
        dto = super().to_dto(file_document)
        if dto and "file" in dto:
            del dto["file"]

        return dto
