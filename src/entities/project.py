from dataclasses import dataclass
from typing import Optional

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.generic_entity import GenericEntity


@dataclass
class Project(GenericEntity):
    budget: Optional[float]

    def __post_init__(self):
        if self.budget and self.budget < 0:
            raise InvalidEntityException("Project", ["budget"])
