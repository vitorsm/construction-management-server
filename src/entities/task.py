from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.expense import Expense
from src.entities.generic_entity import GenericEntity
from src.entities.project import Project
from src.entities.user import User


class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


@dataclass
class TaskHistory:
    id: UUID
    created_at: datetime
    created_by: User
    progress: float
    status: TaskStatus
    files: List[UUID]
    notes: Optional[str]

    # transient
    task: Optional['Task'] = None


    def __post_init__(self):
        invalid_fields = []
        if not self.status:
            invalid_fields.append("status")

        if invalid_fields:
            raise InvalidEntityException("TaskHistory", invalid_fields)

    def set_creating_fields(self, user: User):
        self.id = uuid4()
        self.created_by = user
        self.created_at = datetime.now()


@dataclass
class Task(GenericEntity):
    planned_start_date: Optional[datetime]
    planned_end_date: Optional[datetime]
    actual_start_date: Optional[datetime]
    actual_end_date: Optional[datetime]
    status: TaskStatus
    progress: float
    files: List[str]
    task_history: List[TaskHistory]
    project: Project
    parent_task_id: Optional[UUID]
    expenses: List[Expense] = None

    # transient
    children_tasks: Optional[List['Task']] = None

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")

        if not self.workspace or not self.workspace.id:
            invalid_fields.append("workspace")

        if not self.project or not self.project.id:
            invalid_fields.append("project")

        if self.planned_start_date and self.planned_end_date:
            if self.planned_start_date > self.planned_end_date:
                invalid_fields.append("planned_start_date")
                invalid_fields.append("planned_end_date")

        if self.actual_start_date and self.actual_end_date:
            if self.actual_start_date > self.actual_end_date:
                invalid_fields.append("actual_start_date")
                invalid_fields.append("actual_end_date")

        if not (isinstance(self.progress, int) or isinstance(self.progress, float)) or self.progress < 0 or self.progress > 100:
            invalid_fields.append("progress")

        if not self.status:
            invalid_fields.append("status")

        return invalid_fields

    def add_task_history(self, task_history: TaskHistory):
        self.progress = task_history.progress
        self.task_history.append(task_history)
        self.status = task_history.status

    def add_child_task(self, task: 'Task'):
        if self.children_tasks is None:
            self.children_tasks = []

        self.children_tasks.append(task)

    def get_expenses_value(self) -> float:
        self_expense_values = sum(expense.value for expense in self.expenses) if self.expenses else 0

        if self.children_tasks:
            for child_task in self.children_tasks:
                self_expense_values += child_task.get_expenses_value()

        return self_expense_values

