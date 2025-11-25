from datetime import datetime

from src.adapters.postgres.postgres_task_repository import PostgresTaskRepository
from src.entities.task import Task, TaskStatus
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_integration_test import BaseIntegrationTest
from tests.mocks import task_mock, SECOND_DEFAULT_ID


class TestPostgresTaskRepository(GenericEntityRepositoryTest, BaseIntegrationTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresTaskRepository(self.db_engine)

    def get_repository(self) -> PostgresTaskRepository:
        return self.repository

    def get_first_entity(self) -> Task:
        return task_mock.get_default_task()

    def get_second_entity(self) -> Task:
        task = self.get_first_entity()
        task.id = SECOND_DEFAULT_ID
        task.name = "Task 2"
        task.progress = 0
        task.status = TaskStatus.TODO
        task.planned_start_date = None
        task.planned_end_date = None
        task.actual_start_date = None
        task.actual_end_date = None
        return task

    def get_changed_entity(self) -> Task:
        task = self.get_first_entity()
        task.actual_end_date = None
        task.actual_start_date = datetime.now()
        task.progress = 75
        task.status = TaskStatus.IN_PROGRESS
        return task

    def assert_entity_equal(self, entity1: Task, entity2: Task):
        self.assertEqual(entity1.progress, entity2.progress)
        self.assertEqual(entity1.status, entity2.status)
        self.assertEqual(entity1.planned_start_date, entity2.planned_start_date)
        self.assertEqual(entity1.planned_end_date, entity2.planned_end_date)
        self.assertEqual(entity1.actual_start_date, entity2.actual_start_date)
        self.assertEqual(entity1.actual_end_date, entity2.actual_end_date)
