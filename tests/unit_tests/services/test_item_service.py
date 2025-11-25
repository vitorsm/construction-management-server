from unittest import TestCase
from unittest.mock import Mock

from src.entities.generic_entity import GenericEntity
from src.entities.item import Item
from src.service.generic_service import GenericService
from src.service.item_service import ItemService
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.item_repository import ItemRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from tests.mocks import item_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestItemService(GenericServiceTest, TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec_set=AuthenticationRepository)
        self.workspace_repository = Mock(spec_set=WorkspaceRepository)
        self.item_repository = Mock(spec_set=ItemRepository)

        self.service = ItemService(self.authentication_repository, self.workspace_repository, self.item_repository)

        self.valid_item = item_mock.get_valid_item()

        super().setUp()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.item_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def get_workspace_repository(self) -> Mock:
        return self.workspace_repository

    def get_valid_entity(self) -> GenericEntity:
        return self.valid_item

    def get_changed_entity(self) -> GenericEntity:
        entity = Item(**self.valid_item.__dict__)
        entity.unit_of_measurement = "g"
        entity.name = "Material 2"
        return entity

    def get_different_entity(self) -> GenericEntity:
        return item_mock.get_valid_item()
