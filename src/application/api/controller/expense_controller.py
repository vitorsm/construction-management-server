from flask import Blueprint
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers.expense_mapper import ExpenseMapper
from src.service.expense_service import ExpenseService


class ExpenseController(GenericEntityController[ExpenseService, ExpenseMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("expense_controller", __name__, url_prefix="/api/expenses")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        pass
