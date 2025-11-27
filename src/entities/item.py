from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.entities.generic_entity import GenericEntity


@dataclass
class Item(GenericEntity):
    unit_of_measurement: str

    @staticmethod
    def obj_id(item_id: UUID) -> 'Item':
        item = object.__new__(Item)
        item.id = item_id
        return item

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []
        if not self.name:
            invalid_fields.append("name")

        if not self.workspace or not self.workspace.id:
            invalid_fields.append("workspace")

        if not self.unit_of_measurement:
            invalid_fields.append("unit_of_measurement")

        return invalid_fields
