from datetime import datetime

from sqlalchemy import Column, DateTime, String, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship

from src.adapters.postgres.dto import Base
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.task import Task, TaskStatus, TaskHistory
from src.utils import enum_utils


class TaskHistoryDB(Base[TaskHistory]):

    __tablename__ = "task_history"
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    progress = Column(Float, nullable=False)
    task_id = Column(UUID, ForeignKey("task.id"), nullable=False)
    created_by = Column(UUID, ForeignKey("user.id"), nullable=False)
    notes = Column(String, nullable=True)

    created_by_db = relationship("UserDB", foreign_keys=[created_by], lazy="joined")
    # files: List[str]

    def __init__(self, task_history: TaskHistory, task: Task):
        self.update_attributes(task_history)
        self.task_id = task.id

    def update_attributes(self, task_history: TaskHistory):
        self.id = task_history.id
        self.created_at = task_history.created_at
        self.progress = task_history.progress
        self.created_by = task_history.created_by.id
        self.notes = task_history.notes

    def to_entity(self) -> TaskHistory:
        created_by = self.created_by_db.to_entity()

        return TaskHistory(id=self.id, created_at=self.created_at, progress=self.progress,
                           files=[], created_by=created_by, notes=self.notes)



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
