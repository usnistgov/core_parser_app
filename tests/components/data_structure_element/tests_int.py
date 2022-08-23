""" Integration test of Data structure element
"""
from unittest.mock import Mock

from django.http import HttpRequest

from core_main_app.commons import exceptions
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from tests.components.data_structure_element.fixtures.fixtures import (
    DataStructureElementFixtures,
)


class TestDataStructureElementGetById(MongoIntegrationBaseTestCase):
    """Test Data Structure Element Get By Id"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

    def test_data_get_by_id_raises_does_not_exist_error_if_not_found(self):
        """test_data_get_by_id_raises_does_not_exist_error_if_not_found"""

        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.fixtures.default_owner_with_perm
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_element_api.get_by_id(-1, mock_request)

    def test_data_get_by_id_return_data_if_found(self):
        """test_data_get_by_id_return_data_if_found"""

        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.fixtures.default_owner_with_perm
        # Act
        result = data_structure_element_api.get_by_id(
            self.fixtures.data_structure_element_collection["2000"].id, mock_request
        )
        # Assert
        self.assertEqual(
            result, self.fixtures.data_structure_element_collection["2000"]
        )

    def test_data_get_by_id_raises_exception_if_fail(self):
        """test_data_get_by_id_raises_exception_if_fail"""

        mock_request = Mock(spec=HttpRequest)
        # Act # Assert
        with self.assertRaises(Exception):
            data_structure_element_api.get_by_id("", mock_request)


class TestDataStructureElementGetByXpath(MongoIntegrationBaseTestCase):
    """Test Data Structure Element Get By Xpath"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.user = self.fixtures.default_owner_with_perm
        self.mock_request = Mock(spec=HttpRequest)
        self.mock_request.user = self.fixtures.default_owner_with_perm

        self.fixtures.insert_data(user=self.user)

    def test_data_get_by_xpath_return_data_if_found(self):
        """test_data_get_by_xpath_return_data_if_found"""

        # Act
        expected_element = self.fixtures.data_structure_element_collection["1121"]
        result = data_structure_element_api.get_by_xpath(
            expected_element.options["xpath"]["xml"], self.mock_request
        )
        # Assert
        self.assertEqual(result[0], expected_element)

    def test_data_get_by_xpath_return_empty_if_xpath_not_found(self):
        """test_data_get_by_xpath_return_empty_if_xpath_not_found"""

        # Act
        result = data_structure_element_api.get_by_xpath(
            "wrong_xpath_value", self.mock_request
        )
        # Act
        self.assertEqual(result.count(), 0)


class TestDataStructureElementGetRootElement(MongoIntegrationBaseTestCase):
    """Test Data Structure Element Get Root Element"""

    def setUp(self):
        """setUp"""

        self.fixtures = DataStructureElementFixtures()
        self.fixtures.insert_data()

    def test_get_root_element_returns_root_for_leaf(self):
        """test_get_root_element_returns_root_for_leaf"""

        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.fixtures.default_owner_with_perm

        # Act
        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["1121"], mock_request
        )
        # Assert
        self.assertEqual(
            result, self.fixtures.data_structure_element_collection["root"]
        )

    def test_get_root_element_returns_root_for_branch(self):
        """test_get_root_element_returns_root_for_branch"""

        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.fixtures.default_owner_with_perm

        # Act
        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["1100"], mock_request
        )
        # Assert
        self.assertEqual(
            result, self.fixtures.data_structure_element_collection["root"]
        )

    def test_get_root_element_returns_root_for_root(self):
        """test_get_root_element_returns_root_for_root"""

        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.fixtures.default_owner_with_perm

        # Act
        result = data_structure_element_api.get_root_element(
            self.fixtures.data_structure_element_collection["root"], mock_request
        )
        # Assert
        self.assertEqual(
            result, self.fixtures.data_structure_element_collection["root"]
        )

    def test_get_root_element_return_same_root_for_elements_of_same_tree(self):
        """test_get_root_element_return_same_root_for_elements_of_same_tree"""

        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.fixtures.default_owner_with_perm

        for element in self.fixtures.data_structure_element_collection.values():
            # Act
            result = data_structure_element_api.get_root_element(element, mock_request)
            # Assert
            self.assertEqual(
                result, self.fixtures.data_structure_element_collection["root"]
            )
