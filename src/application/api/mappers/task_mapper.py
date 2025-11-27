from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.task import Task, TaskStatus
from src.entities.user import User
from src.entities.workspace import Workspace
from src.utils import date_utils, enum_utils


class TaskMapper(GenericMapper[Task]):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Task]:
        workspace = Workspace.obj_id(uuid_mapper.to_uuid(dto.get("workspace").get("id"))) if dto.get("workspace") else None
        created_at = date_utils.iso_to_datetime(dto.get("created_at"))
        updated_at = date_utils.iso_to_datetime(dto.get("updated_at"))
        deleted_at = date_utils.iso_to_datetime(dto.get("deleted_at"))
        created_by = User.obj_id(uuid_mapper.to_uuid(dto.get("created_by").get("id"))) if dto.get("created_by") else None
        updated_by = User.obj_id(uuid_mapper.to_uuid(dto.get("updated_by").get("id"))) if dto.get("updated_by") else None
        planned_start_date = date_utils.iso_to_datetime(dto.get("planned_start_date"))
        planned_end_date = date_utils.iso_to_datetime(dto.get("planned_end_date"))
        actual_start_date = date_utils.iso_to_datetime(dto.get("actual_start_date"))
        actual_end_date = date_utils.iso_to_datetime(dto.get("actual_end_date"))
        status = enum_utils.instantiate_enum_from_str_name(TaskStatus, dto.get("status"))

        return Task(id=uuid_mapper.to_uuid(dto.get("id")), name=dto.get("name"), workspace=workspace,
                    created_at=created_at, updated_at=updated_at, deleted_at=deleted_at, created_by=created_by,
                    updated_by=updated_by, planned_start_date=planned_start_date, planned_end_date=planned_end_date,
                    actual_start_date=actual_start_date, actual_end_date=actual_end_date, status=status,
                    progress=dto.get("progress"), files=dto.get("files"), task_history=[])

    @staticmethod
    def to_dto(task: Optional[Task]) -> Optional[dict]:
        if not task:
            return None

        return {
            "id": str(task.id),
            "name": task.name,
            "workspace": {"id": str(task.workspace.id)} if task.workspace else None,
            "created_at": date_utils.datetime_to_iso(task.created_at),
            "updated_at": date_utils.datetime_to_iso(task.updated_at),
            "deleted_at": date_utils.datetime_to_iso(task.deleted_at),
            "created_by": {"id": str(task.created_by.id)} if task.created_by else None,
            "updated_by": {"id": str(task.updated_by.id)} if task.updated_by else None,
            "planned_start_date": date_utils.datetime_to_iso(task.planned_start_date),
            "planned_end_date": date_utils.datetime_to_iso(task.planned_end_date),
            "actual_start_date": date_utils.datetime_to_iso(task.actual_start_date),
            "actual_end_date": date_utils.datetime_to_iso(task.actual_end_date),
            "status": task.status.name,
            "progress": task.progress,
            "files": task.files
        }
