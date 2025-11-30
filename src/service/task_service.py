from datetime import datetime
from multiprocessing.forkserver import set_forkserver_preload
from typing import List
from uuid import UUID

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.task import Task, TaskHistory
from src.entities.task_project_details import TaskProjectDetails
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

        if task.parent_task_id:
            # to check if the parent task id exists
            parent_task = self.find_by_id(task.parent_task_id)
            if parent_task.project != task.project:
                raise InvalidEntityException("Task", ["project"])

    def create_task_history(self, task_id: UUID, task_history: TaskHistory):
        task = self.find_by_id(task_id)
        task.add_task_history(task_history)

        user = self.__authentication_repository.get_current_user()
        task_history.set_creating_fields(user)

        self.__task_repository.create_task_history_and_update_task(task, task_history)

    def find_tasks_by_project(self, project_id: UUID, fill_expenses: bool = False) -> List[Task]:
        # get project to ensure permission and it exists
        project = self.__project_service.find_by_id(project_id)
        return self.__task_repository.find_by_project(project.id, fill_expenses=fill_expenses)

    def find_task_history_by_project(self, project_id: UUID) -> List[TaskHistory]:
        # get project to ensure permission and it exists
        project = self.__project_service.find_by_id(project_id)
        return self.__task_repository.find_task_histories_by_project(project.id)

    def get_task_project_details(self, project_id: UUID) -> TaskProjectDetails:
        return TaskProjectDetails(self.find_tasks_by_project(project_id))
