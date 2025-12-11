import abc
from typing import Generic, TypeVar, get_args, Type, Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto import Base
from src.entities.generic_entity import GenericEntity
from src.service.ports.generic_entity_repository import GenericEntityRepository


Entity = TypeVar("Entity", bound=GenericEntity)
DBModel = TypeVar("DBModel", bound=Base)


class PostgresGenericRepository(GenericEntityRepository, Generic[Entity, DBModel], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_db_instance(self) -> DBInstance:
        raise NotImplementedError

    def get_session(self) -> Session:
        # db_instance = self.get_db_instance()
        # db_engine = db_instance.get_db_engine()
        # return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)()
        return self.get_db_instance().get_session()

    def create(self, entity: Entity):
        model_db_type = self.__get_db_model_type()
        entity_db = model_db_type(entity)
        session = self.get_session()
        session.add(entity_db)
        session.commit()

    def update(self, entity: Entity):
        session = self.get_session()
        entity_db = session.get_one(self.__get_db_model_type(), entity.id)
        entity_db.update_attributes(entity)
        session.commit()

    def delete(self, entity: Entity):
        session = self.get_session()
        entity_db = session.get_one(self.__get_db_model_type(), entity.id)
        session.delete(entity_db)
        session.commit()

    def find_by_id(self, entity_id: UUID) -> Optional[Entity]:
        session = self.get_session()
        model_type = self.__get_db_model_type()

        try:
            entity_db = session.get_one(model_type, entity_id)
        except NoResultFound:
            return None

        # put it in the query
        if hasattr(entity_db, "deleted_at") and entity_db.deleted_at is not None:
            return None

        return entity_db.to_entity()

    def find_all(self, workspace_id: UUID) -> list[Entity]:
        session = self.get_session()
        entity_type = self.__get_db_model_type()
        db_type = self.__get_db_model_type()

        entities_db = (session.query(db_type).filter(and_(entity_type.workspace_id == workspace_id,
                                                                            entity_type.deleted_at == None))
                       .order_by(db_type.name).all())

        return [entity_db.to_entity() for entity_db in entities_db]

    def __get_entity_type(self) -> Type[Entity]:
        return get_args(self.__orig_bases__[0])[0]

    def __get_db_model_type(self) -> Type[DBModel]:
        return get_args(self.__orig_bases__[0])[1]
