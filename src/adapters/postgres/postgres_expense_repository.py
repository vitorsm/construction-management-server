import abc

from flask_sqlalchemy import SQLAlchemy

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.expense_db import ExpenseDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.expense import Expense
from src.service.ports.expense_repository import ExpenseRepository


class PostgresExpenseRepository(PostgresGenericRepository[Expense, ExpenseDB], ExpenseRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
