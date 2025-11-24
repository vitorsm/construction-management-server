from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from src.entities.user import User


@dataclass
class Workspace:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    created_by: User
    updated_by: User

    users_ids: List[UUID]

    def user_has_permission(self, user: User) -> bool:
        return self.users_ids and user.id in self.users_ids
