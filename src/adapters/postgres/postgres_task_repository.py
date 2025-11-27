from flask_sqlalchemy import SQLAlchemy

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.task_db import TaskDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.task import Task
from src.service.ports.task_repository import TaskRepository


class PostgresTaskRepository(PostgresGenericRepository[Task, TaskDB], TaskRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
