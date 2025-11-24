import abc
from typing import TypeVar, Generic, Optional, List, get_args, Dict
from uuid import UUID, uuid4

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.generic_entity import GenericEntity
from src.entities.user import User
from src.entities.workspace import Workspace
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.generic_entity_repository import GenericEntityRepository
from src.service.ports.workspace_repository import WorkspaceRepository

Entity = TypeVar("Entity", bound=GenericEntity)


class GenericService(Generic[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_authentication_repository(self) -> AuthenticationRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def get_workspace_repository(self) -> WorkspaceRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> GenericEntityRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def check_entity(self, entity: Entity):
        raise NotImplementedError

    def create(self, entity: Entity):
        entity.id = uuid4()
        entity.created_at = None
        entity.created_by = None

        self.__write_entity_check(entity)
        self.get_repository().create(entity)

    def update(self, entity: Entity):
        original_entity = self.find_by_id(entity.id)

        if original_entity.workspace != entity.workspace:
            raise InvalidEntityException(self.__get_entity_type_name(), ["workspace"])

        entity.update_original_fields(original_entity)

        self.__write_entity_check(entity)
        self.get_repository().update(entity)

    def delete(self, entity: Entity, is_hard_delete: bool = False):
        original_entity = self.find_by_id(entity.id)
        self.__write_entity_check(original_entity)

        entity.deleted_at = entity.updated_at

        if is_hard_delete:
            self.get_repository().delete(entity)
        else:
            self.get_repository().update(entity)

    def find_by_id(self, entity_id: UUID) -> Optional[Entity]:
        entity = self.get_repository().find_by_id(entity_id)

        if not entity:
            raise EntityNotFoundException(self.__get_entity_type_name(), str(entity_id))

        self.__check_permission(entity, self.get_authentication_repository().get_current_user(), {})

        return entity

    def find_all(self, workspace_id: UUID) -> List[Entity]:
        self.__check_permission_by_workspace(self.get_authentication_repository().get_current_user(), workspace_id, {})
        return self.get_repository().find_all(workspace_id)

    def __write_entity_check(self, entity: Entity):
        current_user = self.get_authentication_repository().get_current_user()
        self.__check_permission(entity, current_user, {})
        self.check_entity(entity)
        entity.update_audit_fields(current_user)

    def __check_permission(self, entity: Entity, user: User, workspace_by_ids: Dict[UUID, Workspace]):
        if not entity.workspace or not entity.workspace.id:
            raise InvalidEntityException(self.__get_entity_type_name(), ["workspace"])

        workspace_id = entity.workspace.id
        workspace = self.__check_permission_by_workspace(user, workspace_id, workspace_by_ids)
        entity.workspace = workspace

    def __check_permission_by_workspace(self, user: User, workspace_id: UUID,
                                        workspace_by_ids: Dict[UUID, Workspace]) -> Workspace:
        if workspace_id in workspace_by_ids:
            workspace = workspace_by_ids[workspace_id]
        else:
            workspace = self.get_workspace_repository().find_by_id(workspace_id)
            workspace_by_ids[workspace_id] = workspace

        if not workspace:
            raise InvalidEntityException(self.__get_entity_type_name(), ["workspace"])

        if not workspace.user_has_permission(user):
            raise PermissionException(workspace, user)

        return workspace

    def __get_entity_type_name(self) -> str:
        return get_args(self.__orig_bases__[0])[0].__name__
