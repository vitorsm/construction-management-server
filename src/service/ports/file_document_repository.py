import abc

from src.service.ports.generic_entity_repository import GenericEntityRepository


class FileDocumentRepository(GenericEntityRepository, metaclass=abc.ABCMeta):
    pass
