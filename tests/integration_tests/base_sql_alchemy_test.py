from unittest import TestCase

from flask import Flask
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.postgres.db_instance import DBInstance
from tests.integration_tests.base_db_integration_test import BaseDBIntegrationTest

test_app = Flask(__name__)


class TestDBInstance(DBInstance):

    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def get_db_engine(self) -> Engine:
        return self.db_engine

    def get_session(self) -> Session:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.db_engine)()



class BaseSQLAlchemyTest(TestCase, BaseDBIntegrationTest):
    def setUp(self):
        self.db_engine = create_engine("sqlite:///:memory:")
        self.db_instance = TestDBInstance(self.db_engine)

        self._init_database()

    def tearDown(self):
        super().clear_database()

    # def __init_database(self):
    #     db_structure_file_path = os.path.join(file_utils.get_project_root(), "resources","db", "init_database.sql")
    #     db_data_file_path = os.path.join(file_utils.get_project_root(), "resources","db", "init_database_load.sql")
    #     self.__execute_sql_file(db_structure_file_path)
    #     self.__execute_sql_file(db_data_file_path)
    #
    # def __execute_sql_file(self, file_path: str):
    #     file = open(file_path)
    #     session = self._get_session()
    #     for query in file.read().split(";"):
    #         query_to_execute = query.strip()
    #
    #         # sqlite uses CURRENT_TIMESTAMP instead of NOW()
    #         query_to_execute = query_to_execute.replace("NOW()", "CURRENT_TIMESTAMP")
    #         # since sqlite doesn't support UUID, we need to change it to TEXT
    #         query_to_execute = query_to_execute.replace("UUID", "TEXT")
    #         # this remove dashes from uuid values, because during the tests it will be inserted without dashes
    #         query_to_execute = query_to_execute.replace("-", "")
    #
    #         if query_to_execute:
    #             session.execute(text(query_to_execute))
    #
    #     session.commit()
    #     file.close()
    #
    # def _get_session(self) -> Session:
    #     return sessionmaker(autocommit=False, autoflush=False, bind=self.db_engine)()
