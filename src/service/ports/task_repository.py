import abc

from src.entities.task import Task, TaskHistory
from src.service.ports.generic_entity_repository import GenericEntityRepository


class TaskRepository(GenericEntityRepository, metaclass=abc.ABCMeta):

    def create_task_history_and_update_task(self, task: Task, task_history: TaskHistory):
        raise NotImplementedError
