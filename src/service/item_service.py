from src.entities.item import Item
from src.service.generic_service import GenericService, Entity
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.item_repository import ItemRepository
from src.service.ports.workspace_repository import WorkspaceRepository


class ItemService(GenericService[Item]):

    def __init__(self, authentication_repository: AuthenticationRepository,
                 workspace_repository: WorkspaceRepository,
                 item_repository: ItemRepository):
        self.__authentication_repository = authentication_repository
        self.__workspace_repository = workspace_repository
        self.__item_repository = item_repository

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_workspace_repository(self) -> WorkspaceRepository:
        return self.__workspace_repository

    def get_repository(self) -> ItemRepository:
        return self.__item_repository

    def check_entity(self, entity: Item):
        pass