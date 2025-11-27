from flask_sqlalchemy import SQLAlchemy

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.project_db import ProjectDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.project import Project
from src.service.ports.project_repository import ProjectRepository


class PostgresProjectRepository(PostgresGenericRepository[Project, ProjectDB], ProjectRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
