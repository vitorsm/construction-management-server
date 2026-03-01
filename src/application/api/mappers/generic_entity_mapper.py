from typing import Dict, Type, Callable, TypeVar

from src.application.api.mappers.generic_mapper import GenericMapper
from src.application.api.mappers.user_mapper import UserMapper
from src.entities.user import User


Entity = TypeVar("Entity")


class GenericEntityMapper(GenericMapper[Entity]):
    test = 1
    @classmethod
    def get_dto_converters(cls) -> Dict[Type, Callable]:
        return {
            User: UserMapper.to_dto,
        }
