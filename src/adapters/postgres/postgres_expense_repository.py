import abc
from typing import List
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

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

    def find_by_project(self, project_id: UUID) -> List[Expense]:
        session = self.get_session()
        expenses_db = session.query(ExpenseDB).filter(
            and_(ExpenseDB.project_id == project_id, ExpenseDB.deleted_at == None)).all()
        return [expense_db.to_entity() for expense_db in expenses_db]

    def find_by_task(self, task_id: UUID) -> List[Expense]:
        session = self.get_session()
        expenses_db = session.query(ExpenseDB).filter(
            and_(ExpenseDB.task_id == task_id, ExpenseDB.deleted_at == None)).all()
        return [expense_db.to_entity() for expense_db in expenses_db]
