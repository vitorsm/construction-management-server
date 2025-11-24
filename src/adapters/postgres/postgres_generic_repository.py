import abc
from typing import Generic, TypeVar, get_args, Type

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.adapters.postgres.dto.generic_entity_db import GenericEntityDB
from src.entities.generic_entity import GenericEntity

Entity = TypeVar("Entity", bound=GenericEntity)
DBModel = TypeVar("DBModel", bound=GenericEntityDB)

class PostgresGenericRepository(Generic[Entity, DBModel], metaclass=abc.ABCMeta):
    db_engine = None

    def get_db_engine(self) -> Engine:
        if not PostgresGenericRepository.db_engine:
            PostgresGenericRepository.db_engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/construction_management")

        return PostgresGenericRepository.db_engine

    def get_session(self) -> Session:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.get_db_engine())()

    def create(self, entity: Entity):
        model_db_type = self.__get_db_model_type()
        entity_db = model_db_type(entity)
        session = self.get_session()
        session.add(entity_db)
        session.commit()

    def __get_entity_type(self) -> Type:
        return get_args(self.__orig_bases__[0])[0]

    def __get_db_model_type(self) -> Type:
        return get_args(self.__orig_bases__[0])[1]
