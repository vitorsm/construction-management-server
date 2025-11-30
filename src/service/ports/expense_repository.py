import abc
from typing import List
from uuid import UUID

from src.entities.expense import Expense
from src.service.ports.generic_entity_repository import GenericEntityRepository


class ExpenseRepository(GenericEntityRepository, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_project(self, project_id: UUID) -> List[Expense]:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_task(self, task_id: UUID) -> List[Expense]:
        raise NotImplementedError
