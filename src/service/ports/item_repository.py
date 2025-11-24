import abc

from src.service.ports.generic_entity_repository import GenericEntityRepository


class ItemRepository(GenericEntityRepository, metaclass=abc.ABCMeta):
    pass
