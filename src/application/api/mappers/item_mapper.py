from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.application.api.mappers.user_mapper import UserMapper
from src.application.api.mappers.workspace_mapper import WorkspaceMapper
from src.entities.item import Item
from src.entities.workspace import Workspace
from src.utils import date_utils


class ItemMapper(GenericMapper[Item]):
    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Item]:
        if not dto:
            return None

        item_id = uuid_mapper.to_uuid(dto.get("id"))
        created_at = date_utils.iso_to_datetime(dto.get("created_at"))
        updated_at = date_utils.iso_to_datetime(dto.get("updated_at"))
        deleted_at = date_utils.iso_to_datetime(dto.get("deleted_at"))
        created_by = UserMapper.to_entity(dto.get("created_by"))
        updated_by = UserMapper.to_entity(dto.get("updated_by"))
        workspace = Workspace.obj_id(uuid_mapper.to_uuid(dto.get("workspace").get("id"))) \
            if dto.get("workspace") else None

        return Item(id=item_id, name=dto.get("name"), created_at=created_at, updated_at=updated_at,
                    deleted_at=deleted_at, created_by=created_by, updated_by=updated_by,
                    unit_of_measurement=dto.get("unit_of_measurement"), workspace=workspace)

    @staticmethod
    def to_dto(entity: Optional[Item]) -> Optional[dict]:
        return {
            "id": str(entity.id),
            "name": entity.name,
            "created_at": date_utils.datetime_to_iso(entity.created_at),
            "updated_at": date_utils.datetime_to_iso(entity.updated_at),
            "deleted_at": date_utils.datetime_to_iso(entity.deleted_at),
            "created_by": UserMapper.to_dto(entity.created_by),
            "updated_by": UserMapper.to_dto(entity.updated_by),
            "unit_of_measurement": entity.unit_of_measurement,
            "workspace": WorkspaceMapper.to_dto(entity.workspace)
        }