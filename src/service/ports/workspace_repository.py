import abc
from typing import Optional, List
from uuid import UUID

from src.entities.workspace import Workspace


class WorkspaceRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_id(self, workspace_id: UUID) -> Optional[Workspace]:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all_workspaces(self) -> List[Workspace]:
        raise NotImplementedError
