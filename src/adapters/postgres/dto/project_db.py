from sqlalchemy import Column, Float

from src.adapters.postgres.dto import Base
from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.project import Project


class ProjectDB(GenericEntityDB, Base[Project]):
    __tablename__ = "project"
    budget = Column(Float, nullable=True)

    def __init__(self, project: Project):
        super().__init__(project)
        self.update_attributes(project)

    def update_attributes(self, project: Project):
        super().update_attributes(project)
        self.budget = project.budget

    def to_entity(self) -> Project:
        project = Project(id=None, name=None, workspace=None, created_at=None,
                          updated_at=None, deleted_at=None, created_by=None,
                          updated_by=None, budget=self.budget)

        self.fill_entity(project)

        return project
