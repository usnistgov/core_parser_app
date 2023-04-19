""" Integration testing for user-side AJAX requests
"""
import json

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.views.user.ajax import data_structure_element_value
from tests import test_settings
from tests.components.data_structure_element.fixtures.fixtures import (
    DataStructureElementFixtures,
)
from tests.views.user.ajax.fixtures import DataStructureElementFixture


class TestGetDataStructureElementValue(IntegrationBaseTestCase):
    """Test Get Data Structure Element Value"""

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
            id=1,
            user=str(self.users["owner"].id),
            tag="mock_tag",
            value="mock_value",
            data_structure=self.fixtures.data_structure,
        )
        request_factory = RequestFactory()
        self.request = request_factory.get(
            reverse("core_parser_app_data_structure_element_value")
        )
        self.request.GET = {
            "id": str(
                self.fixtures.data_structure_element_collection["root"].id
            )
        }

    def test_anonymous_cannot_retrieve_object(self):
        """test_anonymous_cannot_retrieve_object"""

        self.request.user = self.users["anon"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "%s?next=%s"
            % (
                test_settings.LOGIN_URL,
                reverse("core_parser_app_data_structure_element_value"),
            ),
        )

    def test_user_not_owner_cannot_retrieve_object(self):
        """test_user_not_owner_cannot_retrieve_object"""

        self.request.user = self.users["user"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 400)

    def test_owner_can_retrieve_object(self):
        """test_owner_can_retrieve_object"""

        self.request.user = self.users["owner"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content),
            {
                "value": self.fixtures.data_structure_element_collection[
                    "root"
                ].value
            },
        )


class TestPostDataStructureElementValue(IntegrationBaseTestCase):
    """Test Post Data Structure Element Value"""

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

        self.fixture = DataStructureElementFixture()
        self.fixture.insert_data(user=str(self.users["owner"].id))

        request_factory = RequestFactory()
        self.request = request_factory.post(
            reverse("core_parser_app_data_structure_element_value")
        )
        self.request.POST = {
            "id": str(self.fixture.data_structure_element_child.id),
            "value": "mock_value",
        }

    def test_anonymous_cannot_edit_object(self):
        """test_anonymous_cannot_edit_object"""

        self.request.user = self.users["anon"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f'{ test_settings.LOGIN_URL}?next={reverse("core_parser_app_data_structure_element_value")}',
        )

    def test_user_not_owner_cannot_edit_object(self):
        """test_user_not_owner_cannot_edit_object"""

        self.request.user = self.users["user"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 400)

    def test_owner_can_edit_object(self):
        """test_owner_can_edit_object"""

        self.request.user = self.users["owner"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content),
            {"replaced": self.fixture.data_structure_element_child.value},
        )
