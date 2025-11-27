import abc
from uuid import uuid4

from src.adapters.postgres.postgres_generic_repository import PostgresGenericRepository
from src.entities.generic_entity import GenericEntity
from tests.mocks import FIRST_DEFAULT_ID


class GenericEntityRepositoryTest(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_repository(self) -> PostgresGenericRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_entity(self) -> GenericEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_second_entity(self) -> GenericEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_changed_entity(self) -> GenericEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def assert_entity_equal(self, entity1: GenericEntity, entity2: GenericEntity):
        raise NotImplementedError

    def assert_generic_entity_equal(self, entity1: GenericEntity, entity2: GenericEntity):
        self.assertEqual(entity1.id, entity2.id)
        self.assertEqual(entity1.name, entity2.name)
        self.assertEqual(entity1.workspace.id, entity2.workspace.id)
        self.assertEqual(entity1.created_at, entity2.created_at)
        self.assertEqual(entity1.updated_at, entity2.updated_at)
        self.assertEqual(entity1.deleted_at, entity2.deleted_at)
        self.assertEqual(entity1.created_by.id, entity2.created_by.id)
        self.assertEqual(entity1.updated_by.id, entity2.updated_by.id)

        self.assert_entity_equal(entity1, entity2)

    def test_insert_entity(self):
        # given
        entity = self.get_first_entity()
        entity.id = uuid4()

        # when
        self.get_repository().create(entity)

        # then
        persisted_entity = self.get_repository().find_by_id(entity.id)

        self.assertIsNotNone(persisted_entity)
        self.assert_generic_entity_equal(entity, persisted_entity)

    def test_update_entity(self):
        # given
        entity = self.get_changed_entity()
        entity.deleted_at = None

        # when
        self.get_repository().update(entity)

        # then
        persisted_entity = self.get_repository().find_by_id(entity.id)
        self.assert_generic_entity_equal(entity, persisted_entity)

    def test_delete_entity(self):
        # given
        entity = self.get_first_entity()

        # when
        self.get_repository().delete(entity)

        # then
        persisted_entity = self.get_repository().find_by_id(entity.id)
        self.assertIsNone(persisted_entity)

    def test_find_by_id(self):
        # given
        entity_id = FIRST_DEFAULT_ID

        # when
        persisted_entity = self.get_repository().find_by_id(entity_id)

        # then
        entity = self.get_first_entity()
        self.assertIsNotNone(persisted_entity)
        self.assert_generic_entity_equal(entity, persisted_entity)

    def test_find_by_id_not_found(self):
        # given
        random_id = uuid4()

        # when
        entity = self.get_repository().find_by_id(random_id)

        # then
        self.assertIsNone(entity)

    def test_find_all(self):
        # given
        workspace_id = FIRST_DEFAULT_ID

        # then
        persisted_entities = self.get_repository().find_all(workspace_id)

        # when
        first_item = self.get_first_entity()
        second_item = self.get_second_entity()

        self.assertEqual(2, len(persisted_entities))
        self.assert_generic_entity_equal(first_item, persisted_entities[0])
        self.assert_generic_entity_equal(second_item, persisted_entities[1])

    def test_find_all_empty_list(self):
        # given
        random_workspace_id = uuid4()

        # when
        persisted_entities = self.get_repository().find_all(random_workspace_id)

        # then
        self.assertEqual(0, len(persisted_entities))
