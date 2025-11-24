from src.adapters.postgres.dto.project_db import ProjectDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.project import Project


class PostgresProjectRepository(PostgresGenericRepository[Project, ProjectDB]):
    pass
