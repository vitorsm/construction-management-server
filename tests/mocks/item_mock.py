from datetime import datetime
from uuid import uuid4, UUID

from src.entities.item import Item
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import user_mock, workspace_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT

now = datetime.now()


def get_valid_item(iid: UUID = None, name: str = "Item 1", workspace: Workspace = workspace_mock.get_valid_workspace(),
                   created_at: datetime = now, deleted_at: datetime = None, updated_at: datetime = now,
                   created_by: User = user_mock.get_valid_user(), updated_by: User = user_mock.get_valid_user(),
                   unit_of_measure: str = "kg") -> Item:
    iid = iid if iid is not None else uuid4()

    return Item(id=iid, name=name, workspace=workspace, created_at=created_at, updated_at=updated_at, deleted_at=deleted_at,
                created_by=created_by, updated_by=updated_by, unit_of_measurement=unit_of_measure)


def get_default_item() -> Item:
    return get_valid_item(iid=FIRST_DEFAULT_ID,
                          created_by=user_mock.get_default_user(),
                          updated_by=user_mock.get_default_user(),
                          created_at=DEFAULT_CREATED_AT,
                          updated_at=DEFAULT_UPDATED_AT,
                          workspace=workspace_mock.get_default_workspace())
