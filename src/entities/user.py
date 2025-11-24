from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    name: str
    login: str
    password: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
