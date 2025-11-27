from flask import Blueprint, Flask
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers.item_mapper import ItemMapper
from src.service.item_service import ItemService


class ItemController(GenericEntityController[ItemService, ItemMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("item_controller", __name__, url_prefix="/api/items")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        pass