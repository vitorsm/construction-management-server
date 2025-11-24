import abc

from src.service.ports.generic_entity_repository import GenericEntityRepository


class ProjectRepository(GenericEntityRepository, metaclass=abc.ABCMeta):
    pass
