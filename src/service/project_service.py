from src.entities.project import Project
from src.service.generic_service import GenericService, Entity
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.generic_entity_repository import GenericEntityRepository
from src.service.ports.project_repository import ProjectRepository
from src.service.ports.workspace_repository import WorkspaceRepository


class ProjectService(GenericService[Project]):

    def __init__(self, authentication_repository: AuthenticationRepository,
                 workspace_repository: WorkspaceRepository,
                 project_repository: ProjectRepository):
        self.__authentication_repository = authentication_repository
        self.__workspace_repository = workspace_repository
        self.__project_repository = project_repository

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_workspace_repository(self) -> WorkspaceRepository:
        return self.__workspace_repository

    def get_repository(self) -> GenericEntityRepository:
        return self.__project_repository

    def check_entity(self, entity: Project):
        pass
