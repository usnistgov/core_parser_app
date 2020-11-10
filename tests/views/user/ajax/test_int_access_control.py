""" Integration testing for user-side AJAX requests
"""
import json

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.views.user.ajax import data_structure_element_value
from tests import test_settings
from tests.views.user.ajax.fixtures import DataStructureElementFixture


class TestGetDataStructureElementValue(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
        }

        self.fixture = DataStructureElementFixture()
        self.fixture.insert_data()

        request_factory = RequestFactory()
        self.request = request_factory.get(
            reverse("core_parser_app_data_structure_element_value")
        )
        self.request.GET = {"id": str(self.fixture.data_structure_element_child.id)}

    def test_anonymous_cannot_retrieve_object(self):
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
        self.request.user = self.users["user"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 400)

    def test_owner_can_retrieve_object(self):
        self.request.user = self.users["owner"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content),
            {"value": self.fixture.data_structure_element_child.value},
        )


class TestPostDataStructureElementValue(MongoIntegrationBaseTestCase):
    def setUp(self):
        self.users = {
            "anon": AnonymousUser(),
            "user": create_mock_user(user_id=0),
            "owner": create_mock_user(user_id=1),
        }

        self.fixture = DataStructureElementFixture()
        self.fixture.insert_data()

        request_factory = RequestFactory()
        self.request = request_factory.post(
            reverse("core_parser_app_data_structure_element_value")
        )
        self.request.POST = {
            "id": str(self.fixture.data_structure_element_child.id),
            "value": "mock_value",
        }

    def test_anonymous_cannot_edit_object(self):
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

    def test_user_not_owner_cannot_edit_object(self):
        self.request.user = self.users["user"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 400)

    def test_owner_can_edit_object(self):
        self.request.user = self.users["owner"]

        response = data_structure_element_value(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content),
            {"replaced": self.fixture.data_structure_element_child.value},
        )
