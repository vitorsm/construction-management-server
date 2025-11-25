from sqlalchemy import Engine

from src.adapters.postgres.dto.item_db import ItemDB
from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.item import Item
from src.service.ports.item_repository import ItemRepository


class PostgresItemRepository(PostgresGenericRepository[Item, ItemDB], ItemRepository):

    def __init__(self, db_engine: Engine):
        self.__db_engine = db_engine

    def get_db_engine(self) -> Engine:
        return self.__db_engine
