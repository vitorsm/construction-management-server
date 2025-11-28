from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.generic_entity import GenericEntity


@dataclass
class Project(GenericEntity):
    budget: Optional[float]

    @staticmethod
    def obj_id(project_id: UUID) -> 'Project':
        project = object.__new__(Project)
        project.id = project_id
        return project

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []
        if not self.name:
            invalid_fields.append("name")
        if self.budget and self.budget < 0:
            invalid_fields.append("budget")
        if not self.workspace or not self.workspace.id:
            invalid_fields.append("workspace")

        return invalid_fields
