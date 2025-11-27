import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.user import User
from src.entities.workspace import Workspace


@dataclass
class GenericEntity:
    id: UUID
    name: str
    workspace: Workspace
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    created_by: User
    updated_by: User

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @abc.abstractmethod
    def _get_invalid_fields(self) -> List[str]:
        raise NotImplementedError

    def __post_init__(self):
        invalid_fields = self._get_invalid_fields()
        if invalid_fields:
            raise InvalidEntityException("Project", invalid_fields)

    def update_audit_fields(self, user: User):
        self.updated_at = datetime.now()
        self.updated_by = user

        if not self.created_by:
            self.created_by = user
            self.created_at = self.updated_at

    def update_original_fields(self, original_entity: 'GenericEntity'):
        self.created_by = original_entity.created_by
        self.created_at = original_entity.created_at
        self.updated_by = original_entity.updated_by
        self.updated_at = original_entity.updated_at
        self.deleted_at = original_entity.deleted_at
