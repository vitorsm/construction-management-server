import abc
import unittest
from typing import List
from uuid import uuid4

from src.application.api.errors.error_code import ErrorCode
from tests.mocks import SECOND_DEFAULT_ID, FIRST_DEFAULT_ID


class GenericControllerTest(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_valid_entity(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_changed_entity(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_invalid_entity(self) -> List[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def compare_custom_entities(self, entity1: dict, entity2: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def get_address(self, entity_id: str = None) -> str:
        raise NotImplementedError

    def compare_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        if compare_id:
            self.assertEqual(entity1["id"], entity2["id"])

        self.assertEqual(entity1["name"], entity2["name"])
        self.assertEqual(entity1["workspace"]["id"], entity2["workspace"]["id"])
        self.compare_custom_entities(entity1, entity2)

    def assert_tracking_fields(self, entity: dict):
        self.assertIsNotNone(entity["created_at"])
        self.assertIsNotNone(entity["updated_at"])
        self.assertIsNotNone(entity["created_by"])
        self.assertIsNotNone(entity["updated_by"])

    def _remove_tracking_fields_from_dto(self, dto: dict):
        del dto["created_at"]
        del dto["updated_at"]
        del dto["created_by"]
        del dto["updated_by"]

        if "deleted_at" in dto:
            del dto["deleted_at"]

        if "workspace" in dto:
            dto["workspace"] = {"id": dto["workspace"]["id"]}

    def test_create_entity(self):
        # given
        address = self.get_address()
        entity = self.get_valid_entity()
        headers = self.get_default_headers()

        # when
        response = self.client.post(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(201, response.status_code, response.text)
        self.compare_entities(entity, response_data)
        self.assertIsNotNone(response_data["id"])
        self.assert_tracking_fields(response_data)

        address = self.get_address(response_data['id'])
        response = self.client.get(address, headers=headers)
        persisted_entity = response.json
        self.assertEqual(200, response.status_code)
        self.assert_tracking_fields(persisted_entity)
        self.compare_entities(entity, persisted_entity)

    def test_create_invalid_entity(self):
        # given
        address = self.get_address()
        entities = self.get_invalid_entity()
        headers = self.get_default_headers()

        for entity in entities:
            # when
            response = self.client.post(address, json=entity, headers=headers)

            # then
            response_data = response.json
            self.assertEqual(400, response.status_code, response.text)
            self.assertEqual(ErrorCode.VALIDATION_ERROR.value, response_data["code"])
            self.assertIsNotNone(response_data["details"])

    def test_create_without_entity(self):
        # given
        address = self.get_address()
        headers = self.get_default_headers()

        # when
        response = self.client.post(address, json={}, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(400, response.status_code, response.text)
        self.assertEqual(ErrorCode.VALIDATION_ERROR.value, response_data["code"])
        self.assertIsNotNone(response_data["details"])

    def test_create_entity_without_permission(self):
        # given
        address = self.get_address()
        entity = self.get_valid_entity()
        headers = self.get_default_headers(with_permission=False)

        # when
        response = self.client.post(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(403, response.status_code, response.text)
        self.assertEqual(ErrorCode.PERMISSION_ERROR.value, response_data["code"])
        self.assertIn(str(SECOND_DEFAULT_ID), response_data["details"])

    def test_create_entity_without_token(self):
        # given
        address = self.get_address()
        entity = self.get_valid_entity()
        headers = self.get_default_headers(with_token=False)

        # when
        response = self.client.post(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(401, response.status_code, response.text)

    def test_update_entity(self):
        # given
        entity = self.get_valid_entity()
        entity_id = entity["id"]
        address = self.get_address(entity_id)
        headers = self.get_default_headers()

        # when
        response = self.client.put(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(200, response.status_code, response.text)
        self.compare_entities(entity, response_data, compare_id=True)
        self.assert_tracking_fields(response_data)

        address = self.get_address(entity_id)
        response = self.client.get(address, headers=headers)
        persisted_entity = response.json
        self.assertEqual(200, response.status_code)
        self.assert_tracking_fields(persisted_entity)
        self.compare_entities(entity, persisted_entity)

    def test_update_invalid_entity(self):
        # given
        entities = self.get_invalid_entity()

        for entity in entities:
            entity_id = entity["id"]
            address = self.get_address(entity_id)
            headers = self.get_default_headers()

            # when
            response = self.client.put(address, json=entity, headers=headers)

            # then
            response_data = response.json
            self.assertEqual(400, response.status_code, response.text)
            self.assertEqual(ErrorCode.VALIDATION_ERROR.value, response_data["code"])
            self.assertIsNotNone(response_data["details"])

    def test_update_not_found(self):
        # given
        entity = self.get_valid_entity()
        entity_id = str(uuid4())
        entity["id"] = entity_id

        address = self.get_address(entity_id)
        headers = self.get_default_headers()

        # when
        response = self.client.put(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(404, response.status_code, response.text)
        self.assertEqual(ErrorCode.ENTITY_NOT_FOUND.value, response_data["code"])

    def test_update_without_permission(self):
        # given
        entity = self.get_valid_entity()
        entity_id = entity["id"]
        address = self.get_address(entity_id)
        headers = self.get_default_headers(with_permission=False)

        # when
        response = self.client.put(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(403, response.status_code, response.text)
        self.assertEqual(ErrorCode.PERMISSION_ERROR.value, response_data["code"])
        self.assertIsNotNone(response_data["details"])
        self.assertIn(str(SECOND_DEFAULT_ID), response_data["details"])

    def test_update_without_token(self):
        # given
        entity = self.get_valid_entity()
        entity_id = entity["id"]
        address = self.get_address(entity_id)
        headers = self.get_default_headers(with_token=False)

        # when
        response = self.client.put(address, json=entity, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(401, response.status_code, response.text)

    def test_delete_entity(self):
        # given
        entity_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(entity_id)

        # when
        response = self.client.delete(address, headers=self.get_default_headers())

        self.assertEqual(204, response.status_code, response.text)
        response = self.client.get(address, headers=self.get_default_headers())

        self.assertEqual(404, response.status_code, response.text)

    def test_delete_entity_without_permission(self):
        # given
        entity_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(entity_id)

        # when
        response = self.client.delete(address, headers=self.get_default_headers(with_permission=False))

        self.assertEqual(403, response.status_code, response.text)
        self.assertIn(str(SECOND_DEFAULT_ID), response.json["details"])

    def test_delete_entity_without_token(self):
        # given
        entity_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(entity_id)

        # when
        response = self.client.delete(address, headers=self.get_default_headers(with_token=False))

        self.assertEqual(401, response.status_code, response.text)

    def test_delete_entity_not_found(self):
        # given
        entity_id = str(uuid4())
        address = self.get_address(entity_id)

        # when
        response = self.client.delete(address, headers=self.get_default_headers())

        self.assertEqual(404, response.status_code, response.text)

    def test_delete_entity_invalid_id(self):
        # given
        entity_id = "1234123412312341234"
        address = self.get_address(entity_id)

        # when
        response = self.client.delete(address, headers=self.get_default_headers())

        # then
        self.assertEqual(400, response.status_code, response.text)
        self.assertIn("UUID", response.json["details"])

    def test_get_entity(self):
        # given
        entity_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(entity_id)

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(200, response.status_code, response.text)
        entity = self.get_valid_entity()
        persisted_entity = response.json
        self.compare_entities(entity, persisted_entity, compare_id=True)

    def test_get_entity_not_found(self):
        # given
        entity_id = str(uuid4())
        address = self.get_address(entity_id)

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(404, response.status_code, response.text)

    def test_get_entity_invalid_id(self):
        # given
        entity_id = "1234123412312341234"
        address = self.get_address(entity_id)

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(400, response.status_code, response.text)
        self.assertIn("UUID", response.json["details"])

    def test_get_entity_without_permission(self):
        # given
        entity_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(entity_id)

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_permission=False))

        # then
        self.assertEqual(403, response.status_code, response.text)
        self.assertIn(entity_id, response.json["details"])

    def test_get_entity_without_token(self):
        # given
        entity_id = str(FIRST_DEFAULT_ID)
        address = self.get_address(entity_id)

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_token=False))

        # then
        self.assertEqual(401, response.status_code, response.text)

    def test_get_all_entities(self):
        # given
        address = self.get_address()
        address = f"{address}/workspace/{str(FIRST_DEFAULT_ID)}"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(200, response.status_code, response.text)
        entities = response.json
        self.assertEqual(2, len(entities))

    def test_get_all_entities_without_permission(self):
        # given
        address = self.get_address()
        address = f"{address}/workspace/{str(FIRST_DEFAULT_ID)}"

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_permission=False))

        # then
        self.assertEqual(403, response.status_code, response.text)

    def test_get_all_entities_without_token(self):
        # given
        address = self.get_address()
        address = f"{address}/workspace/{str(FIRST_DEFAULT_ID)}"

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_token=False))

        # then
        self.assertEqual(401, response.status_code, response.text)

    @unittest.skip("it was not implemented yet - raise 404 when the workspace doesn't exist")
    def test_get_all_entities_workspace_not_found(self):
        # given
        address = self.get_address()
        address = f"{address}/workspace/{str(uuid4())}"

        # when
        response = self.client.get(address, headers=self.get_default_headers())

        # then
        self.assertEqual(404, response.status_code, response.text)
