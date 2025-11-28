from multiprocessing.forkserver import set_forkserver_preload
from uuid import UUID

from src.entities.task import Task, TaskHistory
from src.service.generic_service import GenericService, Entity
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.generic_entity_repository import GenericEntityRepository
from src.service.ports.task_repository import TaskRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from src.service.project_service import ProjectService


class TaskService(GenericService[Task]):
    def __init__(self, authentication_repository: AuthenticationRepository, workspace_repository: WorkspaceRepository,
                 task_repository: TaskRepository, project_service: ProjectService):
        self.__authentication_repository = authentication_repository
        self.__workspace_repository = workspace_repository
        self.__task_repository = task_repository
        self.__project_service = project_service

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_workspace_repository(self) -> WorkspaceRepository:
        return self.__workspace_repository

    def get_repository(self) -> GenericEntityRepository:
        return self.__task_repository

    def check_entity(self, task: Task):
        task.project = self.__project_service.find_by_id(task.project.id)

    def create_task_history(self, task_id: UUID, task_history: TaskHistory):
        task = self.find_by_id(task_id)
        task.add_task_history(task_history)
        self.__task_repository.create_task_history_and_update_task(task, task_history)
