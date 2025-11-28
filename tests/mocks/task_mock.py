from datetime import datetime, timedelta
from typing import List
from uuid import uuid4, UUID

from src.entities.project import Project
from src.entities.task import Task, TaskStatus, TaskHistory
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import user_mock, workspace_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT, \
    SECOND_DEFAULT_ID, THIRD_DEFAULT_ID, project_mock

now = datetime.now()


def get_valid_task(tid: UUID = None, name: str = "Task 1", workspace: Workspace = workspace_mock.get_valid_workspace(),
                   created_at: datetime = now, updated_at: datetime = now, deleted_at: datetime = None,
                   created_by: User = user_mock.get_valid_user(), updated_by: User = user_mock.get_valid_user(),
                   planned_start_date: datetime = None, planned_end_date: datetime = None, actual_start_date: datetime = None,
                   actual_end_date: datetime = None, status: TaskStatus = TaskStatus.IN_PROGRESS, progress: float = 40,
                   files: List[str] = None, task_history: List[TaskHistory] = None,
                   project: Project = project_mock.get_valid_project()) -> Task:
    tid = tid if tid is not None else uuid4()
    files = files if files is not None else []
    task_history = task_history if task_history is not None else []

    return Task(id=tid, name=name, workspace=workspace, created_at=created_at, updated_at=updated_at, deleted_at=deleted_at,
                created_by=created_by, updated_by=updated_by, planned_start_date=planned_start_date, planned_end_date=planned_end_date,
                actual_start_date=actual_start_date, actual_end_date=actual_end_date, status=status, progress=progress, files=files,
                task_history=task_history, project=project)


def get_task_history(hid: UUID = uuid4(), created_at: datetime = now, progress: float = 15, files: List[str] = None,
                     created_by: User = user_mock.get_valid_user(), notes: str = None,
                     status = TaskStatus.IN_PROGRESS) -> TaskHistory:
    files = files if files is not None else []

    return TaskHistory(id=hid, created_at=created_at, progress=progress,
                       files=files, created_by=created_by, notes=notes, status=status)


def get_default_task() -> Task:
    task_history = [
        get_task_history(hid=FIRST_DEFAULT_ID, created_at=DEFAULT_CREATED_AT, progress=10,
                         created_by=user_mock.get_default_user(), notes="Started working on the task"),
        get_task_history(hid=SECOND_DEFAULT_ID, created_at=DEFAULT_CREATED_AT, progress=40,
                         created_by=user_mock.get_default_user(), notes="Made significant progress"),
        get_task_history(hid=THIRD_DEFAULT_ID, created_at=DEFAULT_CREATED_AT, progress=100,
                         created_by=user_mock.get_default_user(), notes="Task completed successfully"),
    ]

    planned_start_date = DEFAULT_UPDATED_AT + timedelta(days=1)
    planned_end_date = planned_start_date + timedelta(days=1)
    actual_start_date = planned_end_date + timedelta(days=1)
    actual_end_date = actual_start_date + timedelta(days=1)

    return get_valid_task(tid=FIRST_DEFAULT_ID,
                          created_by=user_mock.get_default_user(),
                          updated_by=user_mock.get_default_user(),
                          created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT,
                          workspace=workspace_mock.get_default_workspace(),
                          progress=40, task_history=task_history,
                          planned_start_date=planned_start_date, planned_end_date=planned_end_date,
                          actual_start_date=actual_start_date, actual_end_date=actual_end_date,
                          project=project_mock.get_default_project())
