from datetime import datetime
from uuid import UUID, uuid4

from src.entities.file_document import FileDocument, FileType
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import workspace_mock, user_mock


now = datetime.now()


def get_valid_file_document(fid: UUID = None, name: str = "file",
                            workspace: Workspace = workspace_mock.get_valid_workspace(),
                            created_at: datetime = now, updated_at: datetime = now, deleted_at: datetime = None,
                            created_by: User = user_mock.get_valid_user(),
                            updated_by: User = user_mock.get_valid_user(),
                            file_type: FileType = FileType.PHOTO) -> FileDocument:
    fid = fid if fid else uuid4()

    return FileDocument(id=fid, name=name, workspace=workspace, created_at=created_at, updated_at=updated_at,
                        deleted_at=deleted_at, created_by=created_by, updated_by=updated_by, file_type=file_type)
