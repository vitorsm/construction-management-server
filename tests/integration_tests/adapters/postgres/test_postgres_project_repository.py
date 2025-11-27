from datetime import datetime

from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.adapters.postgres.postgres_project_repository import PostgresProjectRepository
from src.entities.generic_entity import GenericEntity
from src.entities.project import Project
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.mocks import project_mock, user_mock, SECOND_DEFAULT_ID


class TestPostgresProjectRepository(GenericEntityRepositoryTest, BaseSQLAlchemyTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresProjectRepository(self.db_instance)

    def get_repository(self) -> PostgresGenericRepository:
        return self.repository

    def get_first_entity(self) -> Project:
        return project_mock.get_default_project()

    def get_second_entity(self) -> GenericEntity:
        entity = self.get_first_entity()
        entity.id = SECOND_DEFAULT_ID
        entity.name = "Project 2"
        entity.budget = 20000.0

        return entity

    def get_changed_entity(self) -> Project:
        user = user_mock.get_default_user()
        user.id = SECOND_DEFAULT_ID

        project = self.get_first_entity()
        project.name = "new name"
        project.updated_at = datetime.now()
        project.updated_by = user
        project.deleted_at = datetime.now()

        return project

    def assert_entity_equal(self, entity1: Project, entity2: Project):
        self.assertEqual(entity1.budget, entity2.budget)
