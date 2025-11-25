from uuid import uuid4

from src.adapters.postgres.postgres_workspace_repository import PostgresWorkspaceRepository
from tests.integration_tests.base_integration_test import BaseIntegrationTest
from tests.mocks import FIRST_DEFAULT_ID, workspace_mock


class TestPostgresWorkspaceRepository(BaseIntegrationTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresWorkspaceRepository(self.db_engine)

    def test_find_workspace_by_id(self):
        # given
        workspace_id = FIRST_DEFAULT_ID

        # when
        persisted_workspace = self.repository.find_by_id(workspace_id)

        # then
        workspace = workspace_mock.get_default_workspace()

        self.assertIsNotNone(persisted_workspace)
        self.assertEqual(workspace.id, persisted_workspace.id)
        self.assertEqual(workspace.name, persisted_workspace.name)
        self.assertEqual(workspace.created_by, persisted_workspace.created_by)
        self.assertEqual(workspace.updated_by, persisted_workspace.updated_by)
        self.assertEqual(workspace.created_at, persisted_workspace.created_at)
        self.assertEqual(workspace.updated_at, persisted_workspace.updated_at)
        self.assertEqual(workspace.users_ids, persisted_workspace.users_ids)

    def test_find_workspace_by_id_not_found(self):
        # given
        random_workspace_id = uuid4()

        # when
        persisted_workspace = self.repository.find_by_id(random_workspace_id)

        # then
        self.assertIsNone(persisted_workspace)
