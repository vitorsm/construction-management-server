import abc
from typing import TypeVar, Generic, Optional
from uuid import UUID

from src.entities.generic_entity import GenericEntity

Entity = TypeVar("Entity", bound=GenericEntity)


class GenericEntityRepository(Generic[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, entity_id: UUID) -> Optional[Entity]:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self, workspace_id: UUID) -> list[Entity]:
        raise NotImplementedError
