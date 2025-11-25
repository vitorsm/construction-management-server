from sqlalchemy import Engine

from src.adapters.postgres import WorkspaceDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.workspace import Workspace
from src.service.ports.workspace_repository import WorkspaceRepository


class PostgresWorkspaceRepository(PostgresGenericRepository[Workspace, WorkspaceDB], WorkspaceRepository):

    def __init__(self, db_engine: Engine):
        self.__db_engine = db_engine

    def get_db_engine(self) -> Engine:
        return self.__db_engine
