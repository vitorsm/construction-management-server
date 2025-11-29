import abc
from typing import Optional
from uuid import UUID

from src.entities.file_document import FileDocument
from src.service.ports.generic_entity_repository import GenericEntityRepository


class FileDocumentRepository(GenericEntityRepository, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_id(self, file_id: UUID, fill_file: bool = False) -> Optional[FileDocument]:
        raise NotImplementedError
