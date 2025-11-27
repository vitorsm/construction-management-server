from uuid import UUID

from flask_jwt_extended import get_jwt_identity

from src.entities.user import User
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.user_service import UserService


class FlaskAuthenticationRepository(AuthenticationRepository):
    def __init__(self, user_service: UserService):
        self.__user_service = user_service

    def get_current_user(self) -> User:
        user_id = UUID(get_jwt_identity())
        return self.__user_service.find_by_id(user_id)
