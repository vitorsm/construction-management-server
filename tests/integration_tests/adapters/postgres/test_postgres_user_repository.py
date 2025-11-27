from uuid import uuid4

from src.adapters.postgres.postgres_user_repository import PostgresUserRepository
from tests.integration_tests.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.mocks import FIRST_DEFAULT_ID, user_mock


class TestPostgresUserRepository(BaseSQLAlchemyTest):

    def setUp(self):
        super().setUp()
        self.repository = PostgresUserRepository(self.db_instance)

    def test_find_user_by_id(self):
        # given
        user_id = FIRST_DEFAULT_ID

        # when
        persisted_user = self.repository.find_by_id(user_id)

        # then
        user = user_mock.get_default_user()
        self.assertEqual(user.id, persisted_user.id)
        self.assertEqual(user.name, persisted_user.name)
        self.assertEqual(user.login, persisted_user.login)
        self.assertIsNotNone(persisted_user.password)

    def test_find_user_by_id_not_found(self):
        # given
        random_user_id = uuid4()

        # when
        persisted_user = self.repository.find_by_id(random_user_id)

        # then
        self.assertIsNone(persisted_user)

    def test_find_user_by_login(self):
        # given
        user_login = user_mock.get_default_user().login

        # when
        persisted_user = self.repository.find_by_login(user_login)

        # then
        user = user_mock.get_default_user()
        self.assertEqual(user.id, persisted_user.id)
        self.assertEqual(user.name, persisted_user.name)
        self.assertEqual(user.login, persisted_user.login)
        self.assertIsNotNone(persisted_user.password)

    def test_find_user_by_login_not_found(self):
        # given
        wrong_login = "not_existing_login"

        # when
        persisted_user = self.repository.find_by_login(wrong_login)

        # then
        self.assertIsNone(persisted_user)
