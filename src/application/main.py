from datetime import datetime
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.postgres.dto.expense_db import ExpenseDB
from src.adapters.postgres.dto.item_db import ItemDB
from src.adapters.postgres.dto.project_db import ProjectDB
from src.adapters.postgres.dto.task_db import TaskDB
from src.adapters.postgres.dto.user_db import UserDB
from src.adapters.postgres.dto.workspace_db import WorkspaceDB
from src.adapters.postgres.postgres_project_repository import PostgresProjectRepository
from tests.mocks import user_mock, workspace_mock, project_mock, task_mock, expense_mock, item_mock

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/construction_management"

engine = create_engine(DATABASE_URL)

# Base.metadata.create_all(engine)

if __name__ == '__main__':
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as session:
        project_repository = PostgresProjectRepository(engine)
        projects = project_repository.find_all(UUID("f5b9b673-e166-417e-b1a7-5d9f325ce597"))
        print(projects)
        # project_db = session.get_one(ProjectDB, UUID("cc9c3c10-5571-417c-b032-c5ba2c8774f7"))
        # project = project_db.to_entity()
        # # project.name = "updated using repository"
        # project.budget = 11
        # project_repository = PostgresProjectRepository()
        # project_repository.update(project)

    #     user = user_mock.get_valid_user()
    #     new_user = UserDB(user)
    #     session.add(new_user)
    #     session.commit()
    #
    #     workspace = workspace_mock.get_valid_workspace()
    #     workspace.created_by.id = user.id
    #     workspace.updated_by.id = user.id
    #     workspace.users_ids = [user.id]
    #     new_workspace = WorkspaceDB(workspace)
    #     session.add(new_workspace)
    #     session.commit()
    #
    #     workspace_db = session.get_one(WorkspaceDB, workspace.id)
    #     workspace = workspace_db.to_entity()
    #     print(workspace)
    #
    #     project = project_mock.get_valid_project()
    #     project.created_by.id = user.id
    #     project.updated_by.id = user.id
    #     project.workspace.id = workspace.id
    #     project.budget = 10
    #
    #     new_project = ProjectDB(project)
    #     session.add(new_project)
    #     session.commit()
    #
    #     project_db = session.get_one(ProjectDB, project.id)
    #     project = project_db.to_entity()
    #     print(project)
    #
    #     task = task_mock.get_valid_task()
    #     task.created_by.id = user.id
    #     task.updated_by.id = user.id
    #     task.workspace.id = workspace.id
    #     task.planned_start_date = datetime.now()
    #     task.planned_end_date = datetime.now()
    #     task.actual_start_date = datetime.now()
    #     task.actual_end_date = datetime.now()
    #     new_task = TaskDB(task)
    #     session.add(new_task)
    #     session.commit()
    #
    #     task_db = session.get_one(TaskDB, task.id)
    #     task = task_db.to_entity()
    #     print(task)
    #
    #     item = item_mock.get_valid_item()
    #     item.created_by.id = user.id
    #     item.updated_by.id = user.id
    #     item.workspace.id = workspace.id
    #     new_item = ItemDB(item)
    #     session.add(new_item)
    #     session.commit()
    #
    #     expense = expense_mock.get_valid_expense()
    #     expense.created_by.id = user.id
    #     expense.updated_by.id = user.id
    #     expense.items = [item]
    #     expense.workspace.id = workspace.id
    #     new_expense = ExpenseDB(expense)
    #     session.add(new_expense)
    #     session.commit()
    #
    #     expense_db = session.get_one(ExpenseDB, expense.id)
    #     expense = expense_db.to_entity()
    #     print(expense)
