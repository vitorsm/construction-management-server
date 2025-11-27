import abc
from uuid import UUID

from src.entities.user import User


class UserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_login(self, login: str) -> User:
        raise NotImplementedError
