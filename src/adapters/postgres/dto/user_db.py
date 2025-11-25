from sqlalchemy import Column, UUID, String

from src.adapters.postgres.dto import Base, Entity
from src.entities.user import User


class UserDB(Base[User]):
    __tablename__ = "user"
    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=False)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    def __init__(self, user: User):
        self.update_attributes(user)

    def update_attributes(self, user: User):
        self.id = user.id
        self.name = user.name
        self.login = user.login
        self.password = user.password

    def to_entity(self) -> User:
        return User(id=self.id, name=self.name, login=self.login, password=self.password)
