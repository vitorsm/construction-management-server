from unittest.mock import Mock

from src.entities.generic_entity import GenericEntity
from src.entities.project import Project
from src.service.generic_service import GenericService
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.project_repository import ProjectRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from src.service.project_service import ProjectService
from tests.mocks import project_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestProjectService(GenericServiceTest):

    def setUp(self):
        self.authentication_repository = Mock(spec_set=AuthenticationRepository)
        self.workspace_repository = Mock(spec_set=WorkspaceRepository)
        self.project_repository = Mock(spec_set=ProjectRepository)
        self.service = ProjectService(self.authentication_repository, self.workspace_repository,
                                      self.project_repository)
        self.valid_project = project_mock.get_valid_project()
        super().setUp()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.project_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def get_valid_entity(self) -> Project:
        return self.valid_project

    def get_workspace_repository(self) -> Mock:
        return self.workspace_repository

    def get_changed_entity(self) -> GenericEntity:
        changed = Project(**self.valid_project.__dict__)
        changed.name = "new name"
        changed.budget = 10
        return changed

    def get_different_entity(self) -> GenericEntity:
        return project_mock.get_valid_project()
