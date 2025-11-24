from datetime import datetime
from uuid import uuid4

from src.entities.expense import Expense, ExpenseType, ExpenseClass
from tests.mocks import user_mock, workspace_mock, item_mock


def get_valid_expense() -> Expense:
    user = user_mock.get_valid_user()
    now = datetime.now()
    workspace = workspace_mock.get_valid_workspace()
    item = item_mock.get_valid_item()

    return Expense(id=uuid4(), name="Expense 1", workspace=workspace, created_at=now, updated_at=now, deleted_at=None,
                   created_by=user, updated_by=user, expense_type=ExpenseType.MATERIAL,
                   expense_class=ExpenseClass.EXECUTION, items=[item], value=10, files=[], notes=None)
