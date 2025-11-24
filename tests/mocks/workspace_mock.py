from datetime import datetime
from uuid import uuid4

from src.entities.workspace import Workspace
from tests.mocks import user_mock


def get_valid_workspace() -> Workspace:
    now = datetime.now()
    return Workspace(id=uuid4(), name="Workspace1", created_at=now, updated_at=now,
                     created_by=user_mock.get_valid_user(), updated_by=user_mock.get_valid_user(),
                     users_ids=[])
