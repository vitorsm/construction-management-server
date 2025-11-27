from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.user import User


class UserMapper(GenericMapper[User]):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Entity]:
        if not dto:
            return None

        user_id = uuid_mapper.to_uuid(dto.get("id"))
        return User(id=user_id, name=dto.get("name"), login=dto.get("login"), password=dto.get("password"))

    @staticmethod
    def to_dto(user: Optional[User]) -> Optional[dict]:
        if not user:
            return None

        return {
            "id": str(user.id),
            "name": user.name,
            "login": user.login,
            "password": None
        }
