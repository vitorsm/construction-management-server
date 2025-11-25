from sqlalchemy import Engine

from src.adapters.postgres.dto.task_db import TaskDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.task import Task
from src.service.ports.task_repository import TaskRepository


class PostgresTaskRepository(PostgresGenericRepository[Task, TaskDB], TaskRepository):

    def __init__(self, db_engine: Engine):
        self.__db_engine = db_engine

    def get_db_engine(self) -> Engine:
        return self.__db_engine
