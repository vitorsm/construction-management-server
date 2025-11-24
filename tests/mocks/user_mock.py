from uuid import uuid4

from src.entities.user import User


def get_valid_user() -> User:
    return User(id=uuid4(), name="User1", login="user1", password="pass")
