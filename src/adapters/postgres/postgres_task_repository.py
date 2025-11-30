from typing import List
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.task_db import TaskDB, TaskHistoryDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.task import Task, TaskHistory
from src.service.ports.task_repository import TaskRepository


class PostgresTaskRepository(PostgresGenericRepository[Task, TaskDB], TaskRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def create_task_history_and_update_task(self, task: Task, task_history: TaskHistory):
        session = self.get_session()
        task_db = session.get(TaskDB, task.id)
        task_db.update_attributes(task)

        task_history_db = TaskHistoryDB(task_history, task)
        session.add(task_history_db)

        session.commit()

    def find_by_project(self, project_id: UUID, fill_expenses: bool = False) -> List[Task]:
        session = self.get_session()
        tasks_db = session.query(TaskDB).filter(and_(TaskDB.project_id == project_id, TaskDB.deleted_at == None)).all()
        return [task_db.to_entity(fill_expenses=fill_expenses) for task_db in tasks_db]

    def find_task_histories_by_project(self, project_id: UUID) -> List[TaskHistory]:
        session = self.get_session()
        task_histories_db = session.query(TaskHistoryDB).filter(
            and_(TaskHistoryDB.task_db.has(and_(TaskDB.project_id == project_id, TaskDB.deleted_at == None)))
        ).order_by(TaskHistoryDB.created_at.desc()).all()
        return [task_history.to_entity(fill_task=True) for task_history in task_histories_db]
