from datetime import datetime

from sqlalchemy.orm import relationship

from src.adapters.postgres.dto import Base
from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime

from src.adapters.postgres.dto.workspace_users_db import WorkspaceUsersDB
from src.entities.workspace import Workspace


class WorkspaceDB(Base[Workspace]):
    __tablename__ = 'workspace'

    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(UUID, ForeignKey("user.id"), nullable=False)
    updated_by = Column(UUID, ForeignKey("user.id"), nullable=False)

    created_by_db = relationship("UserDB", lazy="select",
                                 primaryjoin="WorkspaceDB.created_by == UserDB.id")
    updated_by_db = relationship("UserDB", lazy="select",
                                 primaryjoin="WorkspaceDB.updated_by == UserDB.id")

    users = relationship("WorkspaceUsersDB", lazy="select",
                         primaryjoin="WorkspaceDB.id == WorkspaceUsersDB.workspace_id")

    def __init__(self, workspace: Workspace):
        self.update_attributes(workspace)

    def update_attributes(self, workspace: Workspace):
        self.id = workspace.id
        self.name = workspace.name
        self.created_at = workspace.created_at
        self.updated_at = workspace.updated_at
        self.created_by = workspace.created_by.id
        self.updated_by = workspace.updated_by.id
        self.users = [WorkspaceUsersDB(self.id, user_id) for user_id in workspace.users_ids]

    def to_entity(self) -> Workspace:
        user_ids = [user_db.user_id for user_db in self.users]
        created_by = self.created_by_db.to_entity()
        updated_by = self.updated_by_db.to_entity()

        return Workspace(id=self.id, name=self.name, created_at=self.created_at, updated_at=self.updated_at,
                         users_ids=user_ids, created_by=created_by, updated_by=updated_by)