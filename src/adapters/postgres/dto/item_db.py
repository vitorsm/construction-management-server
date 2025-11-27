from sqlalchemy import Column, String

from src.adapters.postgres.dto import Base
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.generic_entity import GenericEntity
from src.entities.item import Item


class ItemDB(GenericEntityDB, Base[Item]):
    __tablename__ = "item"
    unit_of_measurement = Column(String, nullable=False)

    def __init__(self, item: Item):
        super().__init__(item)
        self.unit_of_measurement = item.unit_of_measurement

    def update_attributes(self, item: Item):
        super().update_attributes(item)
        self.unit_of_measurement = item.unit_of_measurement

    def to_entity(self) -> Item:
        item = object.__new__(Item)
        item.unit_of_measurement = self.unit_of_measurement

        self.fill_entity(item)
        return item
