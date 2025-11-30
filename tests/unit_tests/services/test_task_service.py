from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.generic_entity import GenericEntity
from src.entities.task import Task, TaskStatus
from src.service.generic_service import GenericService
from src.service.ports.authentication_repository import AuthenticationRepository
from src.service.ports.task_repository import TaskRepository
from src.service.ports.workspace_repository import WorkspaceRepository
from src.service.project_service import ProjectService
from src.service.task_service import TaskService
from tests.mocks import task_mock, project_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestTaskService(GenericServiceTest, TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec_set=AuthenticationRepository)
        self.workspace_repository = Mock(spec_set=WorkspaceRepository)
        self.task_repository = Mock(spec_set=TaskRepository)
        self.project_service = Mock(spec_set=ProjectService)

        self.service = TaskService(self.authentication_repository, self.workspace_repository, self.task_repository,
                                   self.project_service)

        self.valid_task = task_mock.get_valid_task()
        self.valid_project = project_mock.get_valid_project()
        self.project_service.find_by_id.return_value = self.valid_project

        super().setUp()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.task_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def get_workspace_repository(self) -> Mock:
        return self.workspace_repository

    def get_valid_entity(self) -> GenericEntity:
        return self.valid_task

    def get_changed_entity(self) -> GenericEntity:
        task = Task(**self.valid_task.__dict__)
        task.progress = 100
        task.status = TaskStatus.DONE
        return task

    def get_different_entity(self) -> GenericEntity:
        return task_mock.get_valid_task()

    def test_create_task_history(self):
        # given
        task_id = self.valid_task.id
        task_history = task_mock.get_task_history()

        # when
        self.service.create_task_history(task_id, task_history)

        # then
        self.task_repository.create_task_history_and_update_task(self.valid_task, task_history)
        self.assertEqual(task_history.progress, self.valid_task.progress)
        self.assertIsNotNone(task_history.id)
        self.assertEqual(self.current_user, task_history.created_by)
        self.assertIsNotNone(task_history.created_at)

    def test_create_task_history_without_task(self):
        # given
        task_id = self.valid_task.id
        task_history = task_mock.get_task_history()
        self.task_repository.find_by_id.return_value = None

        # when/then
        with self.assertRaises(EntityNotFoundException) as ex:
            self.service.create_task_history(task_id, task_history)

        self.assertIn(str(task_id), str(ex.exception))

    def test_create_task_history_without_permission(self):
        # given
        task_id = self.valid_task.id
        task_history = task_mock.get_task_history()
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.service.create_task_history(task_id, task_history)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_find_tasks_by_project(self):
        # given
        project_id = self.valid_project.id
        tasks = [task_mock.get_valid_task(), task_mock.get_valid_task()]
        self.task_repository.find_by_project.return_value = tasks

        # when
        returned_tasks = self.service.find_tasks_by_project(project_id)

        # then
        self.assertEqual(tasks, returned_tasks)

    def test_find_task_history_by_project(self):
        # given
        project_id = self.valid_project.id
        task_histories = [task_mock.get_task_history()]
        self.task_repository.find_task_histories_by_project(project_id)

    def test_create_task_with_parent(self):
        # given
        task = task_mock.get_valid_task(parent_task_id=uuid4(), project=self.valid_project)
        parent_task = task_mock.get_valid_task(tid=task.parent_task_id, project=self.valid_project)

        self.task_repository.find_by_id.return_value = parent_task

        # when
        self.service.create(task)

        # then
        self.get_repository().create.assert_called_with(task)

    def test_create_task_with_parent_and_different_project(self):
        # given
        task = task_mock.get_valid_task(parent_task_id=uuid4(), project=self.valid_project)
        parent_task = task_mock.get_valid_task(tid=task.parent_task_id)

        self.task_repository.find_by_id.return_value = parent_task

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.service.create(task)

        # then
        self.assertIn("project", str(ex.exception))

    def test_create_task_with_parent_and_not_found(self):
        # given
        task = task_mock.get_valid_task(parent_task_id=uuid4(), project=self.valid_project)
        parent_task = task_mock.get_valid_task(tid=task.parent_task_id, project=self.valid_project)

        self.task_repository.find_by_id.return_value = None

        # when
        with self.assertRaises(EntityNotFoundException) as ex:
            self.service.create(task)

        # then
        self.assertIn(str(parent_task.id), str(ex.exception))
