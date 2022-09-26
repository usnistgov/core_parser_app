from unittest.case import TestCase
from unittest.mock import Mock

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.access_control import (
    _check_data_structure_element_ownership,
)
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)


class TestCheckDataStructureElementOwnership(TestCase):
    """Test Check Data Structure Element Ownership"""

    def setUp(self) -> None:
        self.users = {
            "owner": create_mock_user("1"),
            "random": create_mock_user("2"),
            "anon": create_mock_user("3", is_anonymous=True),
        }
        self.mock_owned_dse = Mock(spec=DataStructureElement)
        self.mock_owned_dse.user = self.users["owner"].id
        self.mock_anon_dse = Mock(spec=DataStructureElement)
        self.mock_anon_dse.user = None

    def test_owned_data_structure_owner_pass(self):
        """test_owned_data_structure_owner_pass"""

        _check_data_structure_element_ownership(
            self.mock_owned_dse, self.users["owner"]
        )

    def test_owned_data_structure_non_owner_fail(self):
        """test_owned_data_structure_non_owner_fail"""

        with self.assertRaises(AccessControlError):
            _check_data_structure_element_ownership(
                self.mock_owned_dse, self.users["random"]
            )

    def test_owned_data_structure_anon_user_fail(self):
        """test_owned_data_structure_anon_user_fail"""

        with self.assertRaises(AccessControlError):
            _check_data_structure_element_ownership(
                self.mock_owned_dse, self.users["anon"]
            )

    def test_anon_data_structure_random_user_pass(self):
        """test_anon_data_structure_random_user_pass"""

        _check_data_structure_element_ownership(
            self.mock_anon_dse, self.users["random"]
        )

    def test_anon_data_structure_anon_user_pass(self):
        """test_anon_data_structure_anon_user_pass"""

        _check_data_structure_element_ownership(
            self.mock_anon_dse, self.users["anon"]
        )
