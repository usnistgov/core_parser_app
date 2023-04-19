""" Integration tests for DataStructureElement API
"""
from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_parser_app.access_control import (
    _check_data_structure_elements_access,
)
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from tests.components.data_structure_element.fixtures.fixtures import (
    DataStructureElementFixtures,
)
from tests.fixtures_utils import MockAnonDataStructure


class TestUpsert(IntegrationBaseTestCase):
    """Test Upsert"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_data_structure_element = DataStructureElement(
            id=10,
            user=str(self.users["owner"].id),
            tag="mock_tag",
            value="mock_value",
            data_structure=self.fixtures.data_structure,
        )

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        """test_anonymous_cannot_perform_operation"""

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
        """test_user_not_owner_cannot_perform_operation"""

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
        """test_owner_can_perform_operation"""

        self.mock_request.user = self.users["owner"]

        data_structure_element_api.upsert(
            self.mock_data_structure_element, self.mock_request
        )

        self.assertEqual(
            data_structure_element_api.get_by_id(
                self.mock_data_structure_element.id, self.mock_request
            ),
            self.mock_data_structure_element,
        )

    def test_superuser_can_perform_operation(self):
        """test_superuser_can_perform_operation"""

        self.mock_request.user = self.users["superuser"]

        data_structure_element_api.upsert(
            self.mock_data_structure_element, self.mock_request
        )

        self.assertEqual(
            data_structure_element_api.get_by_id(
                self.mock_data_structure_element.id, self.mock_request
            ),
            self.mock_data_structure_element,
        )


class TestGetById(IntegrationBaseTestCase):
    """Test Get By Id"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        """test_anonymous_cannot_perform_operation"""

        self.mock_request.user = self.users["anon"]

        with self.assertRaises(DoesNotExist):
            data_structure_element_api.get_by_id(
                self.fixtures.data_structure_element_collection["root"].id,
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        """test_user_not_owner_cannot_perform_operation"""

        self.mock_request.user = self.users["user"]

        with self.assertRaises(DoesNotExist):
            data_structure_element_api.get_by_id(
                self.fixtures.data_structure_element_collection["root"].id,
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        """test_owner_can_perform_operation"""

        self.mock_request.user = self.users["owner"]

        result = data_structure_element_api.get_by_id(
            self.fixtures.data_structure_element_collection["root"].id,
            self.mock_request,
        )
        self.assertEqual(
            result, self.fixtures.data_structure_element_collection["root"]
        )

    def test_superuser_can_perform_operation(self):
        """test_superuser_can_perform_operation"""

        self.mock_request.user = self.users["superuser"]

        result = data_structure_element_api.get_by_id(
            self.fixtures.data_structure_element_collection["root"].id,
            self.mock_request,
        )
        self.assertEqual(
            result, self.fixtures.data_structure_element_collection["root"]
        )


class TestGetByXPath(IntegrationBaseTestCase):
    """Test Get By XPath"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        """test_anonymous_cannot_perform_operation"""

        self.mock_request.user = self.users["anon"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options[
                "xpath"
            ]["xml"],
            self.mock_request,
        )

        self.assertEqual(result.count(), 0)

    def test_user_not_owner_cannot_perform_operation(self):
        """test_user_not_owner_cannot_perform_operation"""

        self.mock_request.user = self.users["user"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options[
                "xpath"
            ]["xml"],
            self.mock_request,
        )

        self.assertEqual(result.count(), 0)

    def test_owner_can_perform_operation(self):
        """test_owner_can_perform_operation"""

        self.mock_request.user = self.users["owner"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options[
                "xpath"
            ]["xml"],
            self.mock_request,
        )

        self.assertEqual(result.count(), 1)
        self.assertEqual(
            result[0], self.fixtures.data_structure_element_collection["1121"]
        )

    def test_superuser_can_perform_operation(self):
        """test_superuser_can_perform_operation"""

        self.mock_request.user = self.users["superuser"]

        result = data_structure_element_api.get_by_xpath(
            self.fixtures.data_structure_element_collection["1121"].options[
                "xpath"
            ]["xml"],
            self.mock_request,
        )

        self.assertEqual(result.count(), 1)
        self.assertEqual(
            result[0], self.fixtures.data_structure_element_collection["1121"]
        )


class TestRemoveChild(IntegrationBaseTestCase):
    """Test Remove Child"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        """test_anonymous_cannot_perform_operation"""

        self.mock_request.user = self.users["anon"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.remove_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.fixtures.data_structure_element_collection["1200"],
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        """test_user_not_owner_cannot_perform_operation"""

        self.mock_request.user = self.users["user"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.remove_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.fixtures.data_structure_element_collection["1200"],
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        """test_owner_can_perform_operation"""

        self.mock_request.user = self.users["owner"]

        orig_children_count = self.fixtures.data_structure_element_collection[
            "1000"
        ].children.count()

        data_structure_element_api.remove_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.fixtures.data_structure_element_collection["1200"],
            self.mock_request,
        )

        self.assertEqual(
            self.fixtures.data_structure_element_collection[
                "1000"
            ].children.count(),
            orig_children_count - 1,
        )

    def test_superuser_can_perform_operation(self):
        """test_superuser_can_perform_operation"""

        self.mock_request.user = self.users["superuser"]

        orig_children_count = self.fixtures.data_structure_element_collection[
            "1000"
        ].children.count()

        data_structure_element_api.remove_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.fixtures.data_structure_element_collection["1200"],
            self.mock_request,
        )

        self.assertEqual(
            self.fixtures.data_structure_element_collection[
                "1000"
            ].children.count(),
            orig_children_count - 1,
        )


class TestAddChild(IntegrationBaseTestCase):
    """Test Add Child"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_data_structure_element = DataStructureElement(
            user=str(self.users["owner"].id),
            tag="mock_tag",
            value="mock_value",
            data_structure=self.fixtures.data_structure,
        )
        self.mock_data_structure_element.save()
        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        """test_anonymous_cannot_perform_operation"""

        self.mock_request.user = self.users["anon"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.add_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.mock_data_structure_element,
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        """test_user_not_owner_cannot_perform_operation"""

        self.mock_request.user = self.users["user"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.add_child(
                self.fixtures.data_structure_element_collection["1000"],
                self.mock_data_structure_element,
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        """test_owner_can_perform_operation"""

        self.mock_request.user = self.users["owner"]

        orig_children_count = self.fixtures.data_structure_element_collection[
            "1000"
        ].children.count()

        data_structure_element_api.add_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.mock_data_structure_element,
            self.mock_request,
        )

        self.assertEqual(
            self.fixtures.data_structure_element_collection[
                "1000"
            ].children.count(),
            orig_children_count + 1,
        )

    def test_superuser_can_perform_operation(self):
        """test_superuser_can_perform_operation"""

        self.mock_request.user = self.users["superuser"]

        orig_children_count = self.fixtures.data_structure_element_collection[
            "1000"
        ].children.count()

        data_structure_element_api.add_child(
            self.fixtures.data_structure_element_collection["1000"],
            self.mock_data_structure_element,
            self.mock_request,
        )

        self.assertEqual(
            self.fixtures.data_structure_element_collection[
                "1000"
            ].children.count(),
            orig_children_count + 1,
        )


class TestGetRootElement(IntegrationBaseTestCase):
    """Test Get Root Element"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_request = Mock(spec=HttpRequest)

    def test_anonymous_cannot_perform_operation(self):
        """test_anonymous_cannot_perform_operation"""

        self.mock_request.user = self.users["anon"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.get_root_element(
                self.fixtures.data_structure_element_collection["1121"],
                self.mock_request,
            )

    def test_user_not_owner_cannot_perform_operation(self):
        """test_user_not_owner_cannot_perform_operation"""

        self.mock_request.user = self.users["user"]

        with self.assertRaises(AccessControlError):
            data_structure_element_api.get_root_element(
                self.fixtures.data_structure_element_collection["1121"],
                self.mock_request,
            )

    def test_owner_can_perform_operation(self):
        """test_owner_can_perform_operation"""

        self.mock_request.user = self.users["owner"]

        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["1121"],
            self.mock_request,
        )

        self.assertEqual(
            result,
            self.fixtures.data_structure_element_collection["root"],
        )

    def test_superuser_can_perform_operation(self):
        """test_superuser_can_perform_operation"""

        self.mock_request.user = self.users["superuser"]

        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["1121"],
            self.mock_request,
        )

        self.assertEqual(
            result,
            self.fixtures.data_structure_element_collection["root"],
        )


class TestDataStructureElementPermissionWithOwners(IntegrationBaseTestCase):
    """Test access to data structure elements when owner is set"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data(user=self.fixtures.default_owner_with_perm)

        self.users = {
            "anon": AnonymousUser(),
            "user": self.fixtures.other_user_with_perm,
            "owner": self.fixtures.default_owner_with_perm,
            "superuser": self.fixtures.superuser,
        }

        self.mock_request = Mock(spec=HttpRequest)

    def test_anon_user_can_not_access_dse_if_permission_and_owner_is_set(self):
        """test_anon_user_can_not_access_dse_if_permission_and_owner_is_set"""

        anon_user_with_perm = AnonymousUser()
        self.mock_request.user = anon_user_with_perm

        with self.assertRaises(AccessControlError):
            _check_data_structure_elements_access(
                [self.fixtures.data_structure_element_collection["root"]],
                anon_user_with_perm,
            )

    def test_owner_can_access_dse_if_permission_and_owner_is_set(self):
        """test_owner_can_access_dse_if_permission_and_owner_is_set"""

        _check_data_structure_elements_access(
            [self.fixtures.data_structure_element_collection["root"]],
            self.users["owner"],
        )

    def test_user_can_not_access_dse_if_permission_and_not_owner(self):
        """test_user_can_not_access_dse_if_permission_and_not_owner"""

        with self.assertRaises(AccessControlError):
            _check_data_structure_elements_access(
                [self.fixtures.data_structure_element_collection["root"]],
                self.users["user"],
            )


class TestDataStructureElementPermissionWithoutOwners(IntegrationBaseTestCase):
    """Test access to data structure elements when owner is not set"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures(add_anon_perm=True)
        self.fixtures.insert_data(
            user=AnonymousUser(), data_structure_class=MockAnonDataStructure
        )

    def test_anon_user_can_access_dse_if_permission_and_no_owner(self):
        """test_anon_user_can_access_dse_if_permission_and_no_owner"""

        _check_data_structure_elements_access(
            [self.fixtures.data_structure_element_collection["root"]],
            AnonymousUser(),
        )


class TestDataStructureElementPermissionWithoutOwnersWithoutPerm(
    IntegrationBaseTestCase
):
    """Test access to data structure elements when owner is not set"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures(add_anon_perm=False)
        self.fixtures.insert_data(user=AnonymousUser())

    def test_anon_user_can_not_access_dse_if_no_permission_and_no_owner(self):
        """test_anon_user_can_not_access_dse_if_no_permission_and_no_owner"""

        with self.assertRaises(AccessControlError):
            _check_data_structure_elements_access(
                [self.fixtures.data_structure_element_collection["root"]],
                AnonymousUser(),
            )
