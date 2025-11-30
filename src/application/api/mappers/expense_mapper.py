from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.expense import Expense, ExpenseType, ExpenseClass
from src.entities.item import Item
from src.entities.project import Project
from src.entities.user import User
from src.entities.workspace import Workspace
from src.utils import enum_utils, date_utils


class ExpenseMapper(GenericMapper[Expense]):
    @staticmethod
    def to_entity(dto: Optional[dict]) -> Optional[Expense]:
        if not dto:
            return None

        workspace = Workspace.obj_id(uuid_mapper.to_uuid(dto.get("workspace").get("id"))) if dto.get("workspace") else None
        expense_type = enum_utils.instantiate_enum_from_str_name(ExpenseType, dto.get("expense_type"))
        expense_class = enum_utils.instantiate_enum_from_str_name(ExpenseClass, dto.get("expense_class"))
        items = [Item.obj_id(uuid_mapper.to_uuid(item_dto.get("id"))) for item_dto in dto.get("items", []) if item_dto.get("id")] if dto.get("items") else []
        created_at = date_utils.iso_to_datetime(dto.get("created_at")) if dto.get("created_at") else None
        updated_at = date_utils.iso_to_datetime(dto.get("updated_at")) if dto.get("updated_at") else None
        deleted_at = date_utils.iso_to_datetime(dto.get("deleted_at")) if dto.get("deleted_at") else None
        created_by = User.obj_id(uuid_mapper.to_uuid(dto.get("created_by").get("id"))) if dto.get("created_by") else None
        updated_by = User.obj_id(uuid_mapper.to_uuid(dto.get("updated_by").get("id"))) if dto.get("updated_by") else None
        project = Project.obj_id(uuid_mapper.to_uuid(dto.get("project").get("id"))) if dto.get("project") else None
        files = [uuid_mapper.to_uuid(file) for file in dto.get("files", [])] if dto.get("files") else []
        task_id = uuid_mapper.to_uuid(dto.get("task_id"))

        return Expense(id=uuid_mapper.to_uuid(dto.get("id")), name=dto.get("name"), workspace=workspace,
                    expense_type=expense_type, expense_class=expense_class, items=items,
                    value=dto.get("value"), files=files, notes=dto.get("notes"),
                    created_at=created_at, updated_at=updated_at, deleted_at=deleted_at,
                    created_by=created_by, updated_by=updated_by, project=project, task_id=task_id)


    @staticmethod
    def to_dto(expense: Optional[Expense]) -> Optional[dict]:
        if not expense:
            return None

        return {
            "id": str(expense.id),
            "name": expense.name,
            "workspace": {"id": str(expense.workspace.id)},
            "project": {"id": str(expense.project.id)},
            "expense_type": expense.expense_type.name,
            "expense_class": expense.expense_class.name,
            "task_id": str(expense.task_id) if expense.task_id else None,
            "items": [{"id": str(item.id), "name": item.name, "unit_of_measurement": item.unit_of_measurement}
                      for item in expense.items] if expense.items else [],
            "value": expense.value,
            "files": [str(file_id) for file_id in expense.files],
            "notes": expense.notes,
            "created_at": date_utils.datetime_to_iso(expense.created_at),
            "updated_at": date_utils.datetime_to_iso(expense.updated_at),
            "deleted_at": date_utils.datetime_to_iso(expense.deleted_at),
            "created_by": {"id": str(expense.created_by.id)},
            "updated_by": {"id": str(expense.updated_by.id)},
        }