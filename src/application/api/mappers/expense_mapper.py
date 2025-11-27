from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.expense import Expense, ExpenseType, ExpenseClass
from src.entities.item import Item
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

        return Expense(id=uuid_mapper.to_uuid(dto.get("id")), name=dto.get("name"), workspace=workspace,
                    expense_type=expense_type, expense_class=expense_class, items=items,
                    value=dto.get("value"), files=dto.get("files", []), notes=dto.get("notes"),
                    created_at=created_at, updated_at=updated_at, deleted_at=deleted_at,
                    created_by=created_by, updated_by=updated_by)


    @staticmethod
    def to_dto(expense: Optional[Expense]) -> Optional[dict]:
        return {
            "id": str(expense.id),
            "name": expense.name,
            "workspace": {"id": str(expense.workspace.id)},
            "expense_type": expense.expense_type.name if expense and expense.expense_type else None,
            "expense_class": expense.expense_class.name if expense and expense.expense_class else None,
            "items": [{"id": str(item.id)} for item in expense.items] if expense and expense.items else [],
            "value": expense.value if expense else None,
            "files": expense.files if expense else [],
            "notes": expense.notes if expense else None,
            "created_at": date_utils.datetime_to_iso(expense.created_at) if expense and expense.created_at else None,
            "updated_at": date_utils.datetime_to_iso(expense.updated_at) if expense and expense.updated_at else None,
            "deleted_at": date_utils.datetime_to_iso(expense.deleted_at) if expense and expense.deleted_at else None,
            "created_by": {"id": str(expense.created_by.id)} if expense and expense.created_by else None,
            "updated_by": {"id": str(expense.updated_by.id)} if expense and expense.updated_by else None,
        }