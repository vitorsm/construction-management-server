from dataclasses import dataclass

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.generic_entity import GenericEntity


@dataclass
class Item(GenericEntity):
    unit_of_measurement: str

    def __post_init__(self):
        if not self.unit_of_measurement:
            raise InvalidEntityException("Item", ["unit_of_measurement"])
