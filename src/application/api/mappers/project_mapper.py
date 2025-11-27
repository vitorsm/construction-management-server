from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.application.api.mappers.user_mapper import UserMapper
from src.application.api.mappers.workspace_mapper import WorkspaceMapper
from src.entities.project import Project
from src.entities.user import User
from src.entities.workspace import Workspace
from src.utils import date_utils


class ProjectMapper(GenericMapper[Project]):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Project]:
        if not dto:
            return None

        project_id = uuid_mapper.to_uuid(dto.get("id"))
        created_by = User.obj_id(uuid_mapper.to_uuid(dto.get("created_by").get("id"))) if dto.get("created_by") else None
        updated_by = User.obj_id(uuid_mapper.to_uuid(dto.get("updated_by").get("id"))) if dto.get("updated_by") else None
        created_at = date_utils.iso_to_datetime(dto.get("created_at"))
        updated_at = date_utils.iso_to_datetime(dto.get("updated_at"))
        deleted_at = date_utils.iso_to_datetime(dto.get("deleted_at"))
        workspace = Workspace.obj_id(uuid_mapper.to_uuid(dto.get("workspace").get("id"))) if dto.get("workspace") else None

        budget = dto.get("budget")

        return Project(
            id=project_id,
            name=dto.get("name"),
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            created_by=created_by,
            updated_by=updated_by,
            workspace=workspace,
            budget=budget
        )


    @staticmethod
    def to_dto(project: Optional[Project]) -> Optional[dict]:
        if not project:
            return None

        return {
            "id": str(project.id),
            "name": project.name,
            "created_at": date_utils.datetime_to_iso(project.created_at),
            "updated_at": date_utils.datetime_to_iso(project.updated_at),
            "deleted_at": date_utils.datetime_to_iso(project.deleted_at),
            "created_by": UserMapper.to_dto(project.created_by),
            "updated_by": UserMapper.to_dto(project.updated_by),
            "workspace": WorkspaceMapper.to_dto(project.workspace),
            "budget": project.budget
        }
