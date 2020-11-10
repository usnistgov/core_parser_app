""" Integration tests for DataStructureElement API
"""
from bson import ObjectId
from django.contrib.auth.models import AnonymousUser
from unittest.mock import Mock

from django.http import HttpRequest

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)

from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)
from tests.components.data_structure_element.fixtures.fixtures import (
    DataStructureElementFixtures,
)


class TestUpsert(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.mock_data_structure_element = DataStructureElement(
            id=ObjectId(), user="1", tag="mock_tag", value="mock_value"
        )

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        # Ensure the call raises an error
        with self.assertRaises(AccessControlError):
            data_structure_element_api.upsert(
                self.mock_data_structure_element, self.mock_request
            )

        # Ensure the object has not been created
        self.mock_request.user = self.users["owner"]
        with self.assertRaises(DoesNotExist):
            data_structure_element_api.get_by_id(
                self.mock_data_structure_element.id, self.mock_request
            )

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        # Ensure the call raises an error
        with self.assertRaises(AccessControlError):
            data_structure_element_api.upsert(
                self.mock_data_structure_element, self.mock_request
            )

        # Ensure the object has not been created
        self.mock_request.user = self.users["owner"]
        with self.assertRaises(DoesNotExist):
            data_structure_element_api.get_by_id(
                self.mock_data_structure_element.id, self.mock_request
            )

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        data_structure_element_api.upsert(
            self.mock_data_structure_element, self.mock_request
        )

        self.assertEquals(
            data_structure_element_api.get_by_id(
                self.mock_data_structure_element.id, self.mock_request
            ),
            self.mock_data_structure_element,
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        data_structure_element_api.upsert(
            self.mock_data_structure_element, self.mock_request
        )

        self.assertEquals(
            data_structure_element_api.get_by_id(
                self.mock_data_structure_element.id, self.mock_request
            ),
            self.mock_data_structure_element,
        )


class TestGetAllByChildId(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        result = list(
            data_structure_element_api.get_all_by_child_id(
                self.fixtures.data_structure_element_collection["1121"].id,
                self.mock_request,
            )
        )

        self.assertEquals(len(result), 0)

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        result = list(
            data_structure_element_api.get_all_by_child_id(
                self.fixtures.data_structure_element_collection["1121"].id,
                self.mock_request,
            )
        )

        self.assertEquals(len(result), 0)

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        result = list(
            data_structure_element_api.get_all_by_child_id(
                self.fixtures.data_structure_element_collection["1121"].id,
                self.mock_request,
            )
        )
        self.assertEquals(len(result), 1)
        self.assertEquals(
            result[0], self.fixtures.data_structure_element_collection["1120"]
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        result = list(
            data_structure_element_api.get_all_by_child_id(
                self.fixtures.data_structure_element_collection["1121"].id,
                self.mock_request,
            )
        )
        self.assertEquals(len(result), 1)
        self.assertEquals(
            result[0], self.fixtures.data_structure_element_collection["1120"]
        )


class TestGetById(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        with self.assertRaises(DoesNotExist):
            data_structure_element_api.get_by_id(
                self.fixtures.data_structure_element_collection["root"].id,
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        with self.assertRaises(DoesNotExist):
            data_structure_element_api.get_by_id(
                self.fixtures.data_structure_element_collection["root"].id,
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        result = data_structure_element_api.get_by_id(
            self.fixtures.data_structure_element_collection["root"].id,
            self.mock_request,
        )
        self.assertEquals(
            result, self.fixtures.data_structure_element_collection["root"]
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        result = data_structure_element_api.get_by_id(
            self.fixtures.data_structure_element_collection["root"].id,
            self.mock_request,
        )
        self.assertEquals(
            result, self.fixtures.data_structure_element_collection["root"]
        )


class TestGetByXPath(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options["xpath"][
                "xml"
            ],
            self.mock_request,
        )

        self.assertEquals(result.count(), 0)

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options["xpath"][
                "xml"
            ],
            self.mock_request,
        )

        self.assertEquals(result.count(), 0)

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options["xpath"][
                "xml"
            ],
            self.mock_request,
        )

        self.assertEquals(result.count(), 1)
        self.assertEquals(
            result[0], self.fixtures.data_structure_element_collection["1121"]
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options["xpath"][
                "xml"
            ],
            self.mock_request,
        )

        self.assertEquals(result.count(), 1)
        self.assertEquals(
            result[0], self.fixtures.data_structure_element_collection["1121"]
        )


class TestRemoveChild(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.remove_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.fixtures.data_structure_element_collection["1200"],
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.remove_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.fixtures.data_structure_element_collection["1200"],
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        orig_children_count = len(
            self.fixtures.data_structure_element_collection["1000"].children
        )

        result = data_structure_element_api.remove_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.fixtures.data_structure_element_collection["1200"],
            self.mock_request,
        )

        self.assertEquals(
            len(result.children),
            orig_children_count - 1,
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        orig_children_count = len(
            self.fixtures.data_structure_element_collection["1000"].children
        )

        result = data_structure_element_api.remove_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.fixtures.data_structure_element_collection["1200"],
            self.mock_request,
        )

        self.assertEquals(
            len(result.children),
            orig_children_count - 1,
        )


class TestAddChild(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.mock_data_structure_element = DataStructureElement(
            user="1", tag="mock_tag", value="mock_value"
        ).save()

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.add_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.mock_data_structure_element,
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.add_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.mock_data_structure_element,
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        orig_children_count = len(
            self.fixtures.data_structure_element_collection["1000"].children
        )

        result = data_structure_element_api.add_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.mock_data_structure_element,
            self.mock_request,
        )

        self.assertEquals(
            len(result.children),
            orig_children_count + 1,
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        orig_children_count = len(
            self.fixtures.data_structure_element_collection["1000"].children
        )

        result = data_structure_element_api.add_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.mock_data_structure_element,
            self.mock_request,
        )

        self.assertEquals(
            len(result.children),
            orig_children_count + 1,
        )


class TestGetRootElement(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
            "superuser": create_mock_user(user_id=2, is_superuser=True),
        }

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        self.mock_request.user = self.users["anon"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.get_root_element(
                self.fixtures.data_structure_element_collection["1121"],
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        self.mock_request.user = self.users["user"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.get_root_element(
                self.fixtures.data_structure_element_collection["1121"],
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        self.mock_request.user = self.users["owner"]

        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["1121"], self.mock_request
        )

        self.assertEquals(
            result,
            self.fixtures.data_structure_element_collection["root"],
        )

    def test_superuser_can_perform_operation(self):
        self.mock_request.user = self.users["superuser"]

        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["1121"], self.mock_request
        )

        self.assertEquals(
            result,
            self.fixtures.data_structure_element_collection["root"],
        )
