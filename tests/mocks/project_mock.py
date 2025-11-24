from datetime import datetime
from uuid import uuid4

from src.entities.project import Project
from tests.mocks import workspace_mock, user_mock


def get_valid_project() -> Project:
    now = datetime.now()
    return Project(id=uuid4(), name="Project 1", workspace=workspace_mock.get_valid_workspace(),
                   created_at=now, updated_at=now, deleted_at=None, created_by=user_mock.get_valid_user(),
                   updated_by=user_mock.get_valid_user(), budget=None)
