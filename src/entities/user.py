from dataclasses import dataclass
from uuid import UUID

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException


@dataclass
class User:
    id: UUID
    name: str
    login: str
    password: str

    @staticmethod
    def obj_id(user_id: UUID) -> 'User':
        user = object.__new__(User)
        user.id = user_id
        return user
    
    def __post_init__(self):
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")

        if not self.login:
            invalid_fields.append("login")

        if invalid_fields:
            raise InvalidEntityException("User", invalid_fields)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
