from dataclasses import dataclass
from enum import Enum
from typing import List

from src.entities.generic_entity import GenericEntity


class FileType(Enum):
    PHOTO = 1


@dataclass
class FileDocument(GenericEntity):
    file_type: FileType

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")
        if not self.file_type:
            invalid_fields.append("file_type")

        return invalid_fields
