from sqlalchemy import Column, DateTime, String, Float

from src.adapters.postgres.dto import Base
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.generic_entity import GenericEntity
from src.entities.task import Task, TaskStatus
from src.utils import enum_utils


class TaskDB(GenericEntityDB, Base[Task]):
    __tablename__ = "task"
    planned_start_date = Column(DateTime, nullable=True)
    planned_end_date = Column(DateTime, nullable=True)
    actual_start_date = Column(DateTime, nullable=True)
    actual_end_date = Column(DateTime, nullable=True)
    status = Column(String(100), nullable=False)
    progress = Column(Float, nullable=False)
    # files: List[str]
    # task_history: List[TaskHistory]

    def __init__(self, task: Task):
        super().__init__(task)
        self.update_attributes(task)

    def update_attributes(self, task: Task):
        super().update_attributes(task)
        self.planned_start_date = task.planned_start_date
        self.planned_end_date = task.planned_end_date
        self.actual_start_date = task.actual_start_date
        self.actual_end_date = task.actual_end_date
        self.status = task.status.name
        self.progress = task.progress

    def to_entity(self) -> Task:
        status = enum_utils.instantiate_enum_from_str_name(TaskStatus, self.status)

        task = Task(id=None, name=None, workspace=None, created_at=None, updated_at=None, deleted_at=None,
                    created_by=None, updated_by=None, planned_start_date=self.planned_start_date,
                    planned_end_date=self.planned_end_date, actual_start_date=self.actual_start_date,
                    actual_end_date=self.actual_end_date, status=status, progress=self.progress,
                    files=[], task_history=[])

        self.fill_entity(task)

        return task
