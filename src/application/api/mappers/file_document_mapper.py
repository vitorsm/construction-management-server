from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.file_document import FileDocument, FileType
from src.entities.user import User
from src.entities.workspace import Workspace
from src.utils import date_utils, enum_utils


class FileDocumentMapper(GenericMapper[FileDocument]):

    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[FileDocument]:
        if not dto:
            return None

        fid = uuid_mapper.to_uuid(dto.get("id"))
        created_at = date_utils.iso_to_datetime(dto.get("created_at"))
        updated_at = date_utils.iso_to_datetime(dto.get("updated_at"))
        deleted_at = date_utils.iso_to_datetime(dto.get("deleted_at"))
        created_by = User.obj_id(uuid_mapper.to_uuid(dto.get("created_by").get("id"))) if dto.get("created_by") else None
        updated_by = User.obj_id(uuid_mapper.to_uuid(dto.get("updated_by").get("id"))) if dto.get("updated_by") else None
        file_type = enum_utils.instantiate_enum_from_str_name(FileType, dto.get("file_type"))
        workspace = Workspace.obj_id(uuid_mapper.to_uuid(dto.get("workspace").get("id"))) if dto.get("workspace") else None

        return FileDocument(id=fid, name=dto.get("name"), created_at=created_at, updated_at=updated_at,
                            deleted_at=deleted_at, created_by=created_by, updated_by=updated_by, file_type=file_type,
                            workspace=workspace, file=None)

    @staticmethod
    def to_dto(file_document: Optional[FileDocument]) -> Optional[dict]:
        if not file_document:
            return None

        return {
            "id": str(file_document.id),
            "name": file_document.name,
            "created_at": date_utils.datetime_to_iso(file_document.created_at),
            "updated_at": date_utils.datetime_to_iso(file_document.updated_at),
            "deleted_at": date_utils.datetime_to_iso(file_document.deleted_at),
            "created_by": {"id": str(file_document.created_by.id)},
            "updated_by": {"id": str(file_document.updated_by.id)},
            "workspace": {"id": str(file_document.workspace.id)},
            "file_type": file_document.file_type.name
        }