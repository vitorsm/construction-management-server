import abc
from typing import TypeVar, Generic, Optional

Entity = TypeVar("Entity")

class GenericMapper(Generic[Entity], metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def to_entity(dto: Optional[dict]) -> Optional[Entity]:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def to_dto(entity: Optional[Entity]) -> Optional[dict]:
        raise NotImplementedError
