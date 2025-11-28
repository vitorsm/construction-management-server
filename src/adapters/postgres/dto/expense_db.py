import uuid

from sqlalchemy import Column, String, Float, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.postgres.dto import Base, Entity
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.expense import Expense, ExpenseType, ExpenseClass
from src.utils import enum_utils


class ExpenseItemDB(Base):
    __tablename__ = "expense_has_item"
    expense_id = Column(UUID, ForeignKey("expense.id"), primary_key=True)
    item_id = Column(UUID, ForeignKey("item.id"), primary_key=True)

    item_db = relationship("ItemDB", foreign_keys=[item_id], lazy="joined")

    def __init__(self, expense_id: uuid.UUID, item_id: uuid.UUID):
        self.expense_id = expense_id
        self.item_id = item_id

    def to_entity(self) -> Entity:
        pass

    def update_attributes(self, entity: Entity):
        pass


class ExpenseDB(GenericEntityDB, Base[Expense]):
    __tablename__ = "expense"
    expense_type = Column(String(100), nullable=False)
    expense_class = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    # files: List[str]
    notes = Column(String, nullable=True)
    project_id = Column(UUID, ForeignKey("project.id"), nullable=True)

    project_db = relationship("ProjectDB", foreign_keys=[project_id], lazy="joined")
    items = relationship("ExpenseItemDB", lazy="select", cascade="all, delete-orphan")

    def __init__(self, expense: Expense):
        super().__init__(expense)
        self.update_attributes(expense)

    def update_attributes(self, expense: Expense):
        super().update_attributes(expense)
        self.expense_type = expense.expense_type.name
        self.expense_class = expense.expense_class.name
        self.value = expense.value
        self.notes = expense.notes
        self.items = [ExpenseItemDB(expense.id, item.id) for item in expense.items]
        self.project_id = expense.project.id

    def to_entity(self) -> Expense:
        expense_type = enum_utils.instantiate_enum_from_str_name(ExpenseType, self.expense_type)
        expense_class = enum_utils.instantiate_enum_from_str_name(ExpenseClass, self.expense_class)
        items = [item.item_db.to_entity() for item in self.items]

        expense = object.__new__(Expense)
        expense.expense_type = expense_type
        expense.expense_class = expense_class
        expense.items = items
        expense.value = self.value
        expense.files = []
        expense.notes = self.notes
        expense.project = self.project_db.to_entity()

        self.fill_entity(expense)
        return expense
