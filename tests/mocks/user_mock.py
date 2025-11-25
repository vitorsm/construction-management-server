from uuid import uuid4, UUID

from src.entities.user import User
from tests.mocks import FIRST_DEFAULT_ID


def get_valid_user() -> User:
    return User(id=uuid4(), name="User1", login="user1", password="pass")


def get_default_user() -> User:
    return User(id=FIRST_DEFAULT_ID, name="User 1", login="user1", password="12345")
