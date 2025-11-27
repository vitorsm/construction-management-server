from typing import List

from flask_sqlalchemy import SQLAlchemy

from src.adapters.postgres import WorkspaceDB
from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.workspace import Workspace
from src.service.ports.workspace_repository import WorkspaceRepository


class PostgresWorkspaceRepository(PostgresGenericRepository[Workspace, WorkspaceDB], WorkspaceRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def find_all_workspaces(self) -> List[Workspace]:
        session = self.get_session()
        entities_db = session.query(self.__get_db_model_type()).filter(WorkspaceDB.users).all()
        return [entity_db.to_entity() for entity_db in entities_db]
