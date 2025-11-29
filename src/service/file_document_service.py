from typing import Optional
from uuid import UUID

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.file_document import FileDocument
from src.service.generic_service import GenericService, Entity
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.file_document_repository import FileDocumentRepository
from src.service.ports.generic_entity_repository import GenericEntityRepository
from src.service.ports.workspace_repository import WorkspaceRepository


class FileDocumentService(GenericService):

    def __init__(self, authentication_repository: AuthenticationRepository, workspace_repository: WorkspaceRepository,
                 file_document_repository: FileDocumentRepository):
        self.__authentication_repository = authentication_repository
        self.__workspace_repository = workspace_repository
        self.__file_document_repository = file_document_repository

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_workspace_repository(self) -> WorkspaceRepository:
        return self.__workspace_repository

    def get_repository(self) -> GenericEntityRepository:
        return self.__file_document_repository

    def check_entity(self, entity: Entity):
        pass

    def find_by_id(self, file_document_id: UUID, fill_file: bool = False) -> Optional[FileDocument]:
        entity = self.__file_document_repository.find_by_id(file_document_id, fill_file=fill_file)

        if not entity:
            raise EntityNotFoundException(self.__get_entity_type_name(), str(file_document_id))

        self._check_permission(entity, self.get_authentication_repository().get_current_user(), {})

        return entity
