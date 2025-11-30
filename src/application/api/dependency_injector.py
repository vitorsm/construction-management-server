from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Binder, singleton

from src.adapters.postgres.db_instance import DBInstance
from src.adapters.postgres.postgres_expense_repository import PostgresExpenseRepository
from src.adapters.postgres.postgres_file_document_repository import PostgresFileDocumentRepository
from src.adapters.postgres.postgres_item_repository import PostgresItemRepository
from src.adapters.postgres.postgres_project_repository import PostgresProjectRepository
from src.adapters.postgres.postgres_task_repository import PostgresTaskRepository
from src.adapters.postgres.postgres_user_repository import PostgresUserRepository
from src.adapters.postgres.postgres_workspace_repository import PostgresWorkspaceRepository
from src.application.api.security.flask_authentication_repository import FlaskAuthenticationRepository
from src.service.expense_service import ExpenseService
from src.service.file_document_service import FileDocumentService
from src.service.item_service import ItemService
from src.service.project_service import ProjectService
from src.service.task_service import TaskService
from src.service.user_service import UserService


class DependencyInjector(Module):
    def __init__(self, app: Flask, db_instance: DBInstance):
        self.app = app
        self.db_instance = db_instance

    def configure(self, binder: Binder):
        expense_repository = PostgresExpenseRepository(self.db_instance)
        item_repository = PostgresItemRepository(self.db_instance)
        project_repository = PostgresProjectRepository(self.db_instance)
        task_repository = PostgresTaskRepository(self.db_instance)
        workspace_repository = PostgresWorkspaceRepository(self.db_instance)
        user_repository = PostgresUserRepository(self.db_instance)
        file_document_repository = PostgresFileDocumentRepository(self.db_instance)

        user_service = UserService(user_repository)

        authentication_repository = FlaskAuthenticationRepository(user_service)

        file_document_service = FileDocumentService(authentication_repository, workspace_repository,
                                                    file_document_repository)
        project_service = ProjectService(authentication_repository, workspace_repository, project_repository)
        item_service = ItemService(authentication_repository, workspace_repository, item_repository)
        task_service = TaskService(authentication_repository, workspace_repository, task_repository, project_service)
        expense_service = ExpenseService(authentication_repository, workspace_repository, expense_repository,
                                         item_service, project_service, task_service)

        binder.bind(UserService, to=user_service, scope=singleton)
        binder.bind(ProjectService, to=project_service, scope=singleton)
        binder.bind(ItemService, to=item_service, scope=singleton)
        binder.bind(ExpenseService, to=expense_service, scope=singleton)
        binder.bind(TaskService, to=task_service, scope=singleton)
        binder.bind(FileDocumentService, to=file_document_service, scope=singleton)
