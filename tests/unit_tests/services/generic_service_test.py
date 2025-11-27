import abc
from unittest.mock import Mock
from uuid import uuid4

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.generic_entity import GenericEntity
from src.service.generic_service import GenericService
from tests.mocks import user_mock, workspace_mock


class GenericServiceTest(metaclass=abc.ABCMeta):

    def setUp(self):
        self.current_user = user_mock.get_valid_user()
        self.user_without_permission = user_mock.get_valid_user()
        self.default_workspace = workspace_mock.get_valid_workspace()
        self.valid_entity = self.get_valid_entity()
        self.changed_entity = self.get_changed_entity()
        self.all_entities = [self.valid_entity, self.get_different_entity()]

        self.valid_entity.workspace = self.default_workspace
        self.changed_entity.workspace = self.default_workspace

        self.default_workspace.users_ids = [self.current_user.id]

        self.get_authentication_repository().get_current_user.return_value = self.current_user
        self.get_workspace_repository().find_by_id.return_value = self.default_workspace
        self.get_repository().find_by_id.return_value = self.valid_entity
        self.get_repository().find_all.return_value = self.all_entities

    @abc.abstractmethod
    def get_service(self) -> GenericService:
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> Mock:
        raise NotImplementedError

    @abc.abstractmethod
    def get_authentication_repository(self) -> Mock:
        raise NotImplementedError

    @abc.abstractmethod
    def get_workspace_repository(self) -> Mock:
        raise NotImplementedError

    @abc.abstractmethod
    def get_valid_entity(self) -> GenericEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_changed_entity(self) -> GenericEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_different_entity(self) -> GenericEntity:
        raise NotImplementedError

    def test_create_entity(self):
        # given
        entity = self.valid_entity
        old_id = entity.id

        # when
        self.get_service().create(entity)

        # then
        self.get_repository().create.assert_called_with(entity)

        self.assertIsNotNone(entity.id)
        self.assertNotEqual(old_id, entity.id)
        self.assertEqual(self.current_user, entity.created_by)
        self.assertEqual(self.current_user, entity.updated_by)
        self.assertEqual(entity.created_at, entity.updated_at)
        self.assertEqual(self.default_workspace, entity.workspace)

    def test_create_without_workspace(self):
        # given
        entity = self.valid_entity
        entity.workspace.id = None

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().create(entity)

        self.assertIn("workspace", str(ex.exception))

    def test_create_with_invalid_workspace(self):
        # given
        entity = self.valid_entity
        self.get_workspace_repository().find_by_id.return_value = None

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().create(entity)

        self.assertIn("workspace", str(ex.exception))

    def test_create_entity_without_permission(self):
        # given
        entity = self.valid_entity
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().create(entity)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_update_entity(self):
        # given
        entity = self.changed_entity
        original_entity = self.valid_entity

        # when
        self.get_service().update(entity)

        # then
        self.get_repository().update.assert_called_with(entity)

        self.assertEqual(original_entity.created_by, entity.created_by)
        self.assertNotEqual(original_entity.updated_by, entity.updated_by)
        self.assertEqual(original_entity.created_at, entity.created_at)
        self.assertNotEqual(original_entity.updated_at, entity.updated_at)
        self.assertEqual(original_entity.workspace, entity.workspace)

    def test_update_entity_not_found(self):
        # given
        entity = self.changed_entity
        self.get_repository().find_by_id.return_value = None

        # when/then
        with self.assertRaises(EntityNotFoundException) as ex:
            self.get_service().update(entity)

        self.assertIn(str(entity.id), str(ex.exception))

    def test_update_entity_different_workspace(self):
        # given
        entity = self.changed_entity
        entity.workspace = workspace_mock.get_valid_workspace()

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(entity)

        self.assertIn("workspace", str(ex.exception))

    def test_update_entity_without_permission(self):
        # given
        entity = self.changed_entity
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().update(entity)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_delete_entity(self):
        # given
        entity = self.valid_entity

        # when
        self.get_service().delete(entity)

        # then
        self.get_repository().update.assert_called_with(entity)

        self.assertEqual(self.current_user, entity.updated_by)
        self.assertNotEqual(entity.created_at, entity.updated_at)
        self.assertIsNotNone(entity.deleted_at)

    def test_hard_delete_entity(self):
        # given
        entity = self.valid_entity

        # when
        self.get_service().delete(entity, is_hard_delete=True)

        # then
        self.get_repository().delete.assert_called_with(entity)

    def test_delete_entity_not_found(self):
        # given
        entity = self.valid_entity
        self.get_repository().find_by_id.return_value = None

        # when/then
        with self.assertRaises(EntityNotFoundException) as ex:
            self.get_service().delete(entity)

        self.assertIn(str(entity.id), str(ex.exception))

    def test_delete_without_permission(self):
        # given
        entity = self.valid_entity
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().delete(entity)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_find_by_id(self):
        # given
        entity_id = self.valid_entity.id

        # when
        entity = self.get_service().find_by_id(entity_id)

        # then
        self.assertEqual(entity_id, entity.id)

    def test_find_by_id_without_permission(self):
        # given
        entity_id = self.valid_entity.id
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().find_by_id(entity_id)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_find_by_id_not_found(self):
        # given
        entity_id = self.valid_entity.id
        self.get_repository().find_by_id.return_value = None

        # when/then
        with self.assertRaises(EntityNotFoundException) as ex:
            self.get_service().find_by_id(entity_id)

        self.assertIn(str(entity_id), str(ex.exception))

    def test_find_all(self):
        # given
        workspace_id = self.default_workspace.id

        # when
        entities = self.get_service().find_all(workspace_id)

        # then
        self.assertEqual(2, len(entities))

    def test_find_all_without_permission(self):
        # given
        workspace_id = self.default_workspace.id
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().find_all(workspace_id)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_find_all_invalid_workspace(self):
        # given
        workspace_id = self.default_workspace.id
        self.get_workspace_repository().find_by_id.return_value = None

        # when/then
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().find_all(workspace_id)

        self.assertIn("workspace", str(ex.exception))
    