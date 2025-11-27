from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.application.api.mappers.user_mapper import UserMapper
from src.entities.workspace import Workspace
from src.utils import date_utils


class WorkspaceMapper(GenericMapper[Workspace]):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Workspace]:
        if not dto:
            return None

        created_by = UserMapper.to_entity(dto.get("created_by"))
        updated_by = UserMapper.to_entity(dto.get("updated_by"))
        created_at = date_utils.iso_to_datetime(dto.get("created_at"))
        updated_at = date_utils.iso_to_datetime(dto.get("updated_at"))
        workspace_id = uuid_mapper.to_uuid(dto.get("id"))
        user_ids = [uuid_mapper.to_uuid(user_id) for user_id in dto.get("users_ids", [])] if dto.get("users_ids") else []

        return Workspace(id=workspace_id, name=dto.get("name"), created_at=created_at, updated_at=updated_at,
                         created_by=created_by, updated_by=updated_by, users_ids=user_ids)

    @staticmethod
    def to_dto(workspace: Optional[Workspace]) -> Optional[dict]:
        if not workspace:
            return None
        
        return {
            "id": str(workspace.id),
            "name": workspace.name,
            "created_at": date_utils.datetime_to_iso(workspace.created_at),
            "updated_at": date_utils.datetime_to_iso(workspace.updated_at),
            "created_by": UserMapper.to_dto(workspace.created_by),
            "updated_by": UserMapper.to_dto(workspace.updated_by),
            "users_ids": [str(user_id) for user_id in workspace.users_ids]
        }
