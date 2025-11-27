from flask_sqlalchemy import SQLAlchemy

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.dto.item_db import ItemDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.item import Item
from src.service.ports.item_repository import ItemRepository


class PostgresItemRepository(PostgresGenericRepository[Item, ItemDB], ItemRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
