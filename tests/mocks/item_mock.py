from datetime import datetime
from uuid import uuid4

from src.entities.item import Item
from tests.mocks import user_mock, workspace_mock


def get_valid_item() -> Item:
    now = datetime.now()
    user = user_mock.get_valid_user()
    workspace = workspace_mock.get_valid_workspace()

    return Item(id=uuid4(), name="Item 1", workspace=workspace, created_at=now, updated_at=now, deleted_at=None,
                created_by=user, updated_by=user, unit_of_measurement="kg")
