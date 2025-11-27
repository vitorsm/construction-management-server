from flask import Blueprint
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers.task_mapper import TaskMapper
from src.service.task_service import TaskService


class TaskController(GenericEntityController[TaskService, TaskMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("task_controller", __name__, url_prefix="/api/tasks")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        pass
