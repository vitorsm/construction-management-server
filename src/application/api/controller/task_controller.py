from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.task_history_mapper import TaskHistoryMapper
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
        @self.get_controller().route("/<string:task_id>/history", methods=["POST"])
        @jwt_required()
        def create_task_history(task_id: str):
            task_uuid = uuid_mapper.to_uuid(task_id)
            dto = request.get_json()
            print(dto)
            task_history = TaskHistoryMapper.to_entity(dto)

            task_service = self.app_injector.get(TaskService)

            task_service.create_task_history(task_uuid, task_history)

            return jsonify(TaskHistoryMapper.to_dto(task_history)), 201
