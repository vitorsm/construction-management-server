import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship

from src.adapters.postgres.dto import Base, Entity
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.task import Task, TaskStatus, TaskHistory
from src.utils import enum_utils


class TaskHistoryFileDB(Base):
    __tablename__ = "task_history_has_file"
    task_history_id = Column(UUID, ForeignKey("task_history.id"), primary_key=True)
    file_document_id = Column(UUID, ForeignKey("file_document.id"), primary_key=True)

    file_document_db = relationship("FileDocumentDB", foreign_keys=[file_document_id], lazy="joined")

    def __init__(self, task_history_id: uuid.UUID, file_document_id: uuid.UUID):
        self.task_history_id = task_history_id
        self.file_document_id = file_document_id

    def to_entity(self) -> Entity:
        pass

    def update_attributes(self, entity: Entity):
        pass


class TaskHistoryDB(Base[TaskHistory]):
    __tablename__ = "task_history"
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    progress = Column(Float, nullable=False)
    task_id = Column(UUID, ForeignKey("task.id"), nullable=False)
    created_by = Column(UUID, ForeignKey("user.id"), nullable=False)
    notes = Column(String, nullable=True)
    status = Column(String, nullable=False)

    created_by_db = relationship("UserDB", foreign_keys=[created_by], lazy="joined")

    files = relationship("TaskHistoryFileDB", lazy="select",
                         primaryjoin="TaskHistoryDB.id == TaskHistoryFileDB.task_history_id")

    task_db = relationship("TaskDB", foreign_keys=[task_id], lazy="joined")

    def __init__(self, task_history: TaskHistory, task: Task):
        self.update_attributes(task_history)
        self.task_id = task.id

    def update_attributes(self, task_history: TaskHistory):
        self.id = task_history.id
        self.created_at = task_history.created_at
        self.progress = task_history.progress
        self.created_by = task_history.created_by.id
        self.notes = task_history.notes
        self.status = task_history.status.name
        self.files = [TaskHistoryFileDB(task_history.id, file_id) for file_id in task_history.files]

    def to_entity(self, fill_task: bool = False) -> TaskHistory:
        created_by = self.created_by_db.to_entity()
        status = enum_utils.instantiate_enum_from_str_name(TaskStatus, self.status)
        files = [file_document.file_document_id for file_document in self.files]
        task = self.task_db.to_entity() if fill_task else None

        return TaskHistory(id=self.id, created_at=self.created_at, progress=self.progress,
                           files=files, created_by=created_by, notes=self.notes, status=status,
                           task=task)


class TaskDB(GenericEntityDB, Base[Task]):
    __tablename__ = "task"
    planned_start_date = Column(DateTime, nullable=True)
    planned_end_date = Column(DateTime, nullable=True)
    actual_start_date = Column(DateTime, nullable=True)
    actual_end_date = Column(DateTime, nullable=True)
    status = Column(String(100), nullable=False)
    progress = Column(Float, nullable=False)
    project_id = Column(UUID, ForeignKey("project.id"), nullable=True)
    parent_task_id = Column(UUID, ForeignKey("task.id"), nullable=False)

    project_db = relationship("ProjectDB", foreign_keys=[project_id], lazy="joined")
    expenses_db = relationship("ExpenseDB", back_populates="task_db")
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
        self.project_id = task.project.id
        self.parent_task_id = task.parent_task_id

    def to_entity(self, fill_expenses: bool = False) -> Task:
        task = object.__new__(Task)
        task.planned_start_date = self.planned_start_date
        task.planned_end_date = self.planned_end_date
        task.actual_start_date = self.actual_start_date
        task.actual_end_date = self.actual_end_date
        task.status = enum_utils.instantiate_enum_from_str_name(TaskStatus, self.status)
        task.progress = self.progress
        task.files = []
        task.task_history = []
        task.project = self.project_db.to_entity()
        task.parent_task_id = self.parent_task_id
        task.expenses = []

        if fill_expenses:
            task.expenses = [expense_db.to_entity() for expense_db in self.expenses_db if expense_db.deleted_at is None]

        self.fill_entity(task)

        return task
