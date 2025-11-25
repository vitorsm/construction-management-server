from datetime import datetime
from uuid import uuid4, UUID

from src.entities.project import Project
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import workspace_mock, user_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT

now = datetime.now()


def get_valid_project(pid: UUID = uuid4(), name: str = "Project 1",
                      workspace: Workspace = workspace_mock.get_valid_workspace(), created_at: datetime = now,
                      updated_at: datetime = now, deleted_at: datetime = None,
                      created_by: User = user_mock.get_valid_user(), updated_by: User = user_mock.get_valid_user(),
                      budget: float = 10000.0) -> Project:
    return Project(id=pid, name=name, workspace=workspace, created_at=created_at, updated_at=updated_at,
                   deleted_at=deleted_at, created_by=created_by, updated_by=updated_by, budget=budget)


def get_default_project() -> Project:
    return get_valid_project(pid=FIRST_DEFAULT_ID,
                             created_by=user_mock.get_default_user(),
                             updated_by=user_mock.get_default_user(),
                             workspace=workspace_mock.get_default_workspace(),
                             created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT)
