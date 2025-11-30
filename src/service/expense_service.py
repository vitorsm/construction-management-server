from typing import List
from uuid import UUID

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.expense import Expense
from src.entities.expense_project_details import ExpenseProjectDetails
from src.service.generic_service import GenericService
from src.service.item_service import ItemService
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.expense_repository import ExpenseRepository
from src.service.ports.generic_entity_repository import GenericEntityRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from src.service.project_service import ProjectService


class ExpenseService(GenericService[Expense]):
    def __init__(self, authentication_repository: AuthenticationRepository, workspace_repository: WorkspaceRepository,
                 expense_repository: ExpenseRepository, item_service: ItemService, project_service: ProjectService):
        self.__authentication_repository = authentication_repository
        self.__workspace_repository = workspace_repository
        self.__expense_repository = expense_repository
        self.__item_service = item_service
        self.__project_service = project_service

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_workspace_repository(self) -> WorkspaceRepository:
        return self.__workspace_repository

    def get_repository(self) -> GenericEntityRepository:
        return self.__expense_repository

    def check_entity(self, expense: Expense):
        if not expense.items:
            return

        expense.project = self.__project_service.find_by_id(expense.project.id)

        new_items = []
        for item in expense.items:
            try:
                persisted_item = self.__item_service.find_by_id(item.id)
            except EntityNotFoundException:
                raise InvalidEntityException("Expense", ["items"])
            except PermissionException:
                raise InvalidEntityException("Expense", ["items"])

            new_items.append(persisted_item)

        expense.items = new_items

    def find_expenses_by_project(self, project_id: UUID) -> List[Expense]:
        # get project to ensure permission and it exists
        project = self.__project_service.find_by_id(project_id)
        return self.__expense_repository.find_by_project(project.id)

    def get_expense_project_details(self, project_id: UUID) -> ExpenseProjectDetails:
        return ExpenseProjectDetails(self.find_expenses_by_project(project_id))
