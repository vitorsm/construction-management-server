from sqlalchemy import Engine

from src.adapters.postgres.dto.expense_db import ExpenseDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.expense import Expense
from src.service.ports.expense_repository import ExpenseRepository


class PostgresExpenseRepository(PostgresGenericRepository[Expense, ExpenseDB], ExpenseRepository):

    def __init__(self, db_engine: Engine):
        self.__db_engine = db_engine

    def get_db_engine(self) -> Engine:
        return self.__db_engine

