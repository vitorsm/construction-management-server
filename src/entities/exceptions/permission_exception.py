
from src.entities.user import User
from src.entities.workspace import Workspace


class PermissionException(Exception):

    def __init__(self, workspace: Workspace, user: User):
        super().__init__(f"User {user.id} does not have permission for workspace {workspace.id}")