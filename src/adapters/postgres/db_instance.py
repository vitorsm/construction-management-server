import abc

from sqlalchemy import Engine


class DBInstance(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_db_engine(self) -> Engine:
        raise NotImplementedError
