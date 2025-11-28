from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.project_mapper import ProjectMapper
from src.application.api.mappers.task_mapper import TaskMapper
from src.service.project_service import ProjectService
from src.service.task_service import TaskService


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

        @self.get_controller().route("/<string:entity_id>/tasks")
        @jwt_required()
        def get_tasks_by_project(entity_id: str):
            uuid_project_id = uuid_mapper.to_uuid(entity_id)

            task_service = self.app_injector.get(TaskService)
            tasks = task_service.find_tasks_by_project(uuid_project_id)
            tasks_dto = [TaskMapper.to_dto(task) for task in tasks]

            return jsonify(tasks_dto)

    def validate_input(self, data: dict):
        pass

