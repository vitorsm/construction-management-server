from datetime import datetime
from uuid import UUID, uuid4

from src.entities.file_document import FileDocument, FileType
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import workspace_mock, user_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT

now = datetime.now()


def get_valid_file_document(fid: UUID = None, name: str = "file",
                            workspace: Workspace = workspace_mock.get_valid_workspace(),
                            created_at: datetime = now, updated_at: datetime = now, deleted_at: datetime = None,
                            created_by: User = user_mock.get_valid_user(),
                            updated_by: User = user_mock.get_valid_user(),
                            file_type: FileType = FileType.PHOTO) -> FileDocument:
    fid = fid if fid else uuid4()

    return FileDocument(id=fid, name=name, workspace=workspace, created_at=created_at, updated_at=updated_at,
                        deleted_at=deleted_at, created_by=created_by, updated_by=updated_by, file_type=file_type,
                        file=None)


def get_default_file_document() -> FileDocument:
    return get_valid_file_document(fid=FIRST_DEFAULT_ID, name="File 1", workspace=workspace_mock.get_default_workspace(),
                                   created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT,
                                   created_by=user_mock.get_default_user(), updated_by=user_mock.get_default_user())
