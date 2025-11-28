import abc
from typing import List
from uuid import UUID

from src.entities.task import Task, TaskHistory
from src.service.ports.generic_entity_repository import GenericEntityRepository


class TaskRepository(GenericEntityRepository, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_task_history_and_update_task(self, task: Task, task_history: TaskHistory):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_project(self, project_id: UUID) -> List[Task]:
        raise NotImplementedError
