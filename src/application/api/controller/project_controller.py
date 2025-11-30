from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.expense_mapper import ExpenseMapper
from src.application.api.mappers.feed_item_mapper import FeedItemMapper
from src.application.api.mappers.generic_mapper import GenericMapper
from src.application.api.mappers.project_dashboard_mapper import ProjectDashboardMapper
from src.application.api.mappers.project_mapper import ProjectMapper
from src.application.api.mappers.task_mapper import TaskMapper
from src.service.expense_service import ExpenseService
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
            tasks = task_service.find_tasks_by_project(uuid_project_id, fill_expenses=True)
            tasks_dto = TaskMapper.to_dtos_tree(tasks)

            return jsonify(tasks_dto)

        @self.get_controller().route("/<string:project_id>/expenses")
        @jwt_required()
        def get_expenses_by_project(project_id: str):
            uuid_project_id = uuid_mapper.to_uuid(project_id)

            expense_service = self.app_injector.get(ExpenseService)
            expenses = expense_service.find_expenses_by_project(uuid_project_id)
            expenses_dto = GenericMapper.to_dtos(expenses, ExpenseMapper.to_dto)

            return jsonify(expenses_dto)

        @self.get_controller().route("/<string:project_id>/feed")
        @jwt_required()
        def get_feed_items(project_id: str):
            uuid_project_id = uuid_mapper.to_uuid(project_id)

            task_service = self.app_injector.get(TaskService)
            task_histories = task_service.find_task_history_by_project(uuid_project_id)
            feed_items = GenericMapper.to_dtos(task_histories, FeedItemMapper.task_history_to_feed_item)

            return jsonify(feed_items)

        @self.get_controller().route("/<string:project_id>/dashboard")
        @jwt_required()
        def get_dashboard(project_id: str):
            uuid_project_id = uuid_mapper.to_uuid(project_id)

            task_service = self.app_injector.get(TaskService)
            expense_service = self.app_injector.get(ExpenseService)

            task_project_details = task_service.get_task_project_details(uuid_project_id)
            expense_project_details = expense_service.get_expense_project_details(uuid_project_id)

            return jsonify(ProjectDashboardMapper.to_dto(task_project_details, expense_project_details))


    def validate_input(self, data: dict):
        pass

