from flask import Blueprint, Flask
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers.project_mapper import ProjectMapper
from src.service.project_service import ProjectService


class ProjectController(GenericEntityController[ProjectService, ProjectMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("project_controller", __name__, url_prefix="/api/projects")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        pass

    def validate_input(self, data: dict):
        pass
