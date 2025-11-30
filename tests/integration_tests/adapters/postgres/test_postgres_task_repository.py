from datetime import datetime
from uuid import uuid4

from src.adapters.postgres import ExpenseDB
from src.adapters.postgres.dto.task_db import TaskHistoryDB
from src.adapters.postgres.postgres_task_repository import PostgresTaskRepository
from src.entities.expense import ExpenseType, ExpenseClass
from src.entities.task import Task, TaskStatus, TaskHistory
from tests.integration_tests.adapters.postgres.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.integration_tests.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.mocks import task_mock, SECOND_DEFAULT_ID, FIRST_DEFAULT_ID, user_mock


class TestPostgresTaskRepository(GenericEntityRepositoryTest, BaseSQLAlchemyTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresTaskRepository(self.db_instance)

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
        task.parent_task_id = FIRST_DEFAULT_ID
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
        self.assertEqual(entity1.project, entity2.project)
        self.assertEqual(entity1.parent_task_id, entity2.parent_task_id)

    def test_find_tasks_by_project(self):
        # given
        project_id = FIRST_DEFAULT_ID

        # when
        tasks = self.repository.find_by_project(project_id, fill_expenses=True)

        # then
        self.assertEqual(2, len(tasks))
        self.assertEqual(FIRST_DEFAULT_ID, tasks[0].id)
        self.assertEqual(SECOND_DEFAULT_ID, tasks[1].id)
        self.assertEqual("Task 1", tasks[0].name)
        self.assertEqual("Task 2", tasks[1].name)
        self.assertEqual(1, len(tasks[0].expenses))
        self.assertEqual("Expense 1", tasks[0].expenses[0].name)
        self.assertEqual(ExpenseType.MATERIAL, tasks[0].expenses[0].expense_type)
        self.assertEqual(ExpenseClass.EXECUTION, tasks[0].expenses[0].expense_class)

    def test_find_tasks_by_project_emtpy(self):
        # given
        project_id = uuid4()

        # when
        tasks = self.repository.find_by_project(project_id)

        # then
        self.assertEqual(0, len(tasks))

    def test_create_task_history(self):
        # given
        task_history = task_mock.get_task_history(notes="text")
        task_history.created_by = user_mock.get_default_user()
        task_history.files = [FIRST_DEFAULT_ID]
        task = task_mock.get_default_task()

        # when
        self.repository.create_task_history_and_update_task(task, task_history)

        # then
        persisted_entity = self._get_session().get_one(TaskHistoryDB, task_history.id)

        self.assertIsNotNone(persisted_entity)
        self.assertEqual(task_history.notes, persisted_entity.notes)
        self.assertEqual(task_history.progress, persisted_entity.progress)
        self.assertEqual(task_history.status.name, persisted_entity.status)
        self.assertEqual(task_history.notes, persisted_entity.notes)
        self.assertEqual(task_history.files[0], persisted_entity.files[0].file_document_id)

    def test_find_task_histories_by_project(self):
        # given
        project_id = FIRST_DEFAULT_ID

        # when
        task_histories = self.repository.find_task_histories_by_project(project_id)

        # then
        self.assertEqual(2, len(task_histories))

    def test_find_task_histories_by_project_empty(self):
        # given
        project_id = uuid4()

        # when
        task_histories = self.repository.find_task_histories_by_project(project_id)

        # then
        self.assertEqual(0, len(task_histories))

    def test_delete_task_with_expense(self):
        # given
        task = task_mock.get_default_task()

        # when
        self.repository.delete(task)

        # then
        expense_db = self._get_session().get_one(ExpenseDB, FIRST_DEFAULT_ID)
        self.assertIsNone(expense_db.task_id)
