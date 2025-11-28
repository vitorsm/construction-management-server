from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.task import TaskHistory, TaskStatus
from src.entities.user import User
from src.utils import date_utils, enum_utils


class TaskHistoryMapper(GenericMapper[TaskHistory]):
    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[TaskHistory]:
        if not dto:
            return None
        created_by = User.obj_id(dto.get("created_by").get("id")) if dto.get("created_by") else None
        created_at = date_utils.iso_to_datetime(dto.get("created_at"))
        tid = uuid_mapper.to_uuid(dto.get("id"))
        files = dto.get("files") or []
        status = enum_utils.instantiate_enum_from_str_name(TaskStatus, dto.get("status"))

        return TaskHistory(id=tid, created_at=created_at, created_by=created_by, progress=dto.get("progress"),
                           files=files, notes=dto.get("notes"), status=status)

    @staticmethod
    def to_dto(task_history: Optional[TaskHistory]) -> Optional[dict]:
        if not task_history:
            return None

        return {
            "id": str(task_history.id),
            "created_by": {"id": task_history.created_by.id},
            "created_at": date_utils.datetime_to_iso(task_history.created_at),
            "progress": task_history.progress,
            "files": task_history.files,
            "notes": task_history.notes,
            "status": task_history.status.name
        }