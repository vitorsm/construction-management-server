from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.generic_entity import GenericEntity
from src.entities.item import Item
from src.entities.project import Project


class ExpenseType(Enum):
    MATERIAL = 1
    SERVICE = 2
    LABOR = 3
    PROJECT = 4
    DOCUMENT = 5
    TRANSPORT = 6


class ExpenseClass(Enum):
    PLANNING = 1
    EXECUTION = 2


@dataclass
class Expense(GenericEntity):
    expense_type: ExpenseType
    expense_class: ExpenseClass
    items: List[Item]
    value: float
    files: List[str]
    notes: Optional[str]
    project: Project

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")
        if not self.workspace or not self.workspace.id:
            invalid_fields.append("workspace")
        if not self.project or not self.project.id:
            invalid_fields.append("project")
        if not self.expense_type:
            invalid_fields.append("expense_type")
        if not self.expense_class:
            invalid_fields.append("expense_class")
        if not self.value:
            invalid_fields.append("value")
        if self.items and any(not item.id for item in self.items):
            invalid_fields.append("items")
        if not isinstance(self.value, (int, float)) or self.value < 0:
            invalid_fields.append("value")

        return invalid_fields
