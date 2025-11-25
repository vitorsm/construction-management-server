from datetime import datetime
from tokenize import String

from sqlalchemy import Column, UUID, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.postgres.dto import Base, Entity
from src.entities.task import TaskHistory, Task


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

    def to_entity(self) -> TaskHistory:
        created_by = self.created_by_db.to_entity()

        return TaskHistory(id=self.id, created_at=self.created_at, progress=self.progress,
                           files=[], created_by=created_by)
