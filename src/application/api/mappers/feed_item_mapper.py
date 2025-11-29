from typing import Optional

from src.application.api.mappers.task_mapper import TaskMapper
from src.application.api.mappers.user_mapper import UserMapper
from src.entities.task import TaskHistory
from src.utils import date_utils


class FeedItemMapper:
    @staticmethod
    def task_history_to_feed_item(task_history: Optional[TaskHistory]) -> Optional[dict]:
        if not task_history:
            return None

        return {
            "id": str(task_history.id),
            "type": "TASK_HISTORY",
            "source": TaskMapper.to_dto(task_history.task),
            "created_at": date_utils.datetime_to_iso(task_history.created_at),
            "created_by": UserMapper.to_dto(task_history.created_by),
            "progress": task_history.progress,
            "status": task_history.status.name,
            "files": task_history.files,
            "notes": task_history.notes
        }