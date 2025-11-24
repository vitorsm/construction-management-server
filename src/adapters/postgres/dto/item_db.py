from sqlalchemy import Column, String

from src.adapters.postgres.dto import Base
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.item import Item


class ItemDB(GenericEntityDB, Base):
    __tablename__ = "item"
    unit_of_measurement = Column(String, nullable=False)

    def __init__(self, item: Item):
        super().__init__(item)
        self.unit_of_measurement = item.unit_of_measurement

    def to_entity(self) -> Item:
        item = Item(id=None, name=None, workspace=None, created_at=None, updated_at=None, deleted_at=None,
                    created_by=None, updated_by=None, unit_of_measurement=self.unit_of_measurement)
        self.fill_entity(item)
        return item
