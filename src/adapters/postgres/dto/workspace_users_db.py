from sqlalchemy import Column, UUID, ForeignKey

from src.adapters.postgres.dto import Base, Entity


class WorkspaceUsersDB(Base):
    __tablename__ = "workspace_has_user"
    workspace_id = Column(UUID, ForeignKey("workspace.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)

    def __init__(self, workspace_id: UUID, user_id: UUID):
        self.workspace_id = workspace_id
        self.user_id = user_id

    def to_entity(self) -> Entity:
        pass

    def update_attributes(self, entity: Entity):
        pass
