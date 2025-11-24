from datetime import datetime
from uuid import uuid4

from src.entities.task import Task, TaskStatus, TaskHistory
from tests.mocks import user_mock, workspace_mock


def get_valid_task() -> Task:
    user = user_mock.get_valid_user()
    workspace = workspace_mock.get_valid_workspace()
    now = datetime.now()

    return Task(id=uuid4(), name="Task 1", workspace=workspace, created_at=now, updated_at=now, deleted_at=None,
                created_by=user, updated_by=user, planned_start_date=None, planned_end_date=None,
                actual_start_date=None, actual_end_date=None, status=TaskStatus.IN_PROGRESS, progress=10, files=[],
                task_history=[])


def get_task_history() -> TaskHistory:
    return TaskHistory(id=uuid4(), created_at=datetime.now(), progress=15,
                       files=[])
