import abc
from typing import TypeVar, Generic, Optional, Iterator, List, Callable

Entity = TypeVar("Entity")

class GenericMapper(Generic[Entity], metaclass=abc.ABCMeta):

    @staticmethod
    def to_entities(dtos: Iterator[dict], entity_convert_func: Callable) -> List[Entity]:
        if not dtos:
            return []

        return [entity_convert_func(dto) for dto in dtos]

    @staticmethod
    def to_dtos(entities: Iterator[Entity], dto_convert_func: Callable) -> List[dict]:
        if not entities:
            return []

        return [dto_convert_func(entity) for entity in entities]

    @staticmethod
    @abc.abstractmethod
    def to_entity(dto: Optional[dict]) -> Optional[Entity]:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def to_dto(entity: Optional[Entity]) -> Optional[dict]:
        raise NotImplementedError
