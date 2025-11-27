from typing import List

from flask import Flask
from flask_jwt_extended import JWTManager
from injector import Injector

from src.application.api import AuthenticationController, ProjectController, ItemController
from src.application.api.controller.expense_controller import ExpenseController
from src.application.api.controller.task_controller import TaskController
from src.application.api.errors import exception_handler


def instantiate_controllers(app: Flask, app_injector: Injector):
    jwt_manager = JWTManager(app)
    controllers = []

    authentication_controller = AuthenticationController(app_injector)
    controllers.append(authentication_controller.controller)

    project_controller = ProjectController(app_injector)
    controllers.append(project_controller.controller)

    item_controller = ItemController(app_injector)
    controllers.append(item_controller.controller)

    task_controller = TaskController(app_injector)
    controllers.append(task_controller.controller)

    expense_controller = ExpenseController(app_injector)
    controllers.append(expense_controller.controller)

    exception_handler.error_handlers(controllers)
    for controller in controllers:
        app.register_blueprint(controller)

