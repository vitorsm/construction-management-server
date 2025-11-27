from uuid import UUID

from src.entities.exceptions.authentication_exception import AuthenticationException
from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.user import User
from src.service.ports.user_repository import UserRepository
from src.utils import encryption_utils


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def find_by_id(self, user_id: UUID) -> User:
        user = self.__user_repository.find_by_id(user_id)

        if not user:
            raise EntityNotFoundException("User", str(user_id))

        return user

    def authenticate(self, login: str, password: str) -> User:

        user = self.__user_repository.find_by_login(login)
        if not user or not encryption_utils.check_encrypted_password(password, user.password):
            raise AuthenticationException(login)

        return user
