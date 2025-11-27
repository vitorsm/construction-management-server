from flask_sqlalchemy import SQLAlchemy

from src.adapters.postgres import UserDB
from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.user import User
from src.service.ports.user_repository import UserRepository


class PostgresUserRepository(PostgresGenericRepository[User, UserDB], UserRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def find_by_login(self, login: str) -> User:
        session = self.get_session()
        user_db = session.query(UserDB).filter(UserDB.login == login).first()
        return user_db.to_entity() if user_db else None
