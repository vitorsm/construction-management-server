from datetime import datetime

from sqlalchemy import Column, UUID, DateTime, Float, ForeignKey

from src.adapters.postgres.dto import Base
from src.entities.task import TaskHistory, Task


class TaskHistoryDB(Base):
    __tablename__ = "task_history"
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    progress = Column(Float, nullable=False)
    task_id = Column(UUID, ForeignKey("task.id"), nullable=False)
    # files: List[str]

    def __init__(self, task_history: TaskHistory, task: Task):
        self.id = task_history.id
        self.created_at = task_history.created_at
        self.progress = task_history.progress
        self.task_id = task.id

    def to_entity(self) -> TaskHistory:
        return TaskHistory(id=self.id, created_at=self.created_at, progress=self.progress,
                           files=[])
