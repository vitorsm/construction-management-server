from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.generic_entity import GenericEntity
from src.entities.item import Item



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

    def __post_init__(self):
        invalid_fields = []

        if not self.expense_type:
            invalid_fields.append("expense_type")
        if not self.expense_class:
            invalid_fields.append("expense_class")
        if not self.value:
            invalid_fields.append("value")

        if invalid_fields:
            raise InvalidEntityException("Expense", invalid_fields)
