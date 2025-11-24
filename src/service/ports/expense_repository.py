import abc

from src.service.ports.generic_entity_repository import GenericEntityRepository


class ExpenseRepository(GenericEntityRepository, metaclass=abc.ABCMeta):
    pass
