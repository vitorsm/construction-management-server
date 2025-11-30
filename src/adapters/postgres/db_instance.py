import abc

from sqlalchemy import Engine
from sqlalchemy.orm import Session


class DBInstance(metaclass=abc.ABCMeta):

    # @abc.abstractmethod
    # def get_db_engine(self) -> Engine:
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError

