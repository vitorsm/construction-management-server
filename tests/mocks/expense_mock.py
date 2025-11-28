from datetime import datetime
from typing import List
from uuid import uuid4, UUID

from src.entities.expense import Expense, ExpenseType, ExpenseClass
from src.entities.item import Item
from src.entities.project import Project
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import user_mock, workspace_mock, item_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT, \
    project_mock

now = datetime.now()


def get_valid_expense(eid: UUID = None, name: str = "Expense 1",
                      workspace: Workspace = workspace_mock.get_valid_workspace(), created_at: datetime = now,
                      updated_at: datetime = now, deleted_at: datetime = None,
                      created_by: User = user_mock.get_valid_user(), updated_by: User = user_mock.get_valid_user(),
                      expense_type: ExpenseType = ExpenseType.MATERIAL,
                      expense_class: ExpenseClass = ExpenseClass.EXECUTION, items: List[Item] = None,
                      value: float = 10, files: List = None, notes: str = None,
                      project: Project = project_mock.get_valid_project()) -> Expense:
    eid = eid if eid is not None else eid
    items = items if items is not None else [item_mock.get_valid_item()]
    files = files if files is not None else []


    return Expense(id=eid, name=name, workspace=workspace, created_at=created_at, updated_at=updated_at, deleted_at=deleted_at,
                   created_by=created_by, updated_by=updated_by, expense_type=expense_type,
                   expense_class=expense_class, items=items, value=value, files=files, notes=notes, project=project)


def get_default_expense() -> Expense:
    return get_valid_expense(eid=FIRST_DEFAULT_ID, created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT,
                             created_by=user_mock.get_default_user(), updated_by=user_mock.get_default_user(),
                             workspace=workspace_mock.get_default_workspace(),
                             value=100, notes="Initial expense", items=[item_mock.get_default_item()],
                             project=project_mock.get_default_project())
