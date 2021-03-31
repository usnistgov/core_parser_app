""" Unit Test Data Structure Element
"""
from unittest.case import TestCase
from unittest.mock import Mock

from django.http import HttpRequest
from mock import patch

import core_parser_app.components.data_structure_element.api as data_structure_element_api
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


class TestDataStructureElementGetById(TestCase):
    @patch.object(DataStructureElement, "get_by_id")
    def test_data_structure_element_get_by_id_raises_does_not_exist_error_if_not_found(
        self, mock_get
    ):
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_element_api.get_by_id(1, mock_request)

    def test_data_structure_element_get_by_id_raises_model_error_if_not_found(self):
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.ModelError):
            data_structure_element_api.get_by_id(1, mock_request)

    @patch.object(DataStructureElement, "get_by_id")
    def test_data_structure_element_get_by_id_return_data_if_found(self, mock_get):
        # Arrange
        mock_data_structure_element = DataStructureElement(
            user="1", tag="tag", value="value"
        )
        mock_get.return_value = mock_data_structure_element

        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")
        # Act
        result = data_structure_element_api.get_by_id(1, mock_request)
        # Assert
        self.assertIsInstance(result, DataStructureElement)


class TestDataStructureElementGetByXpath(TestCase):
    @patch.object(DataStructureElement, "get_by_xpath")
    def test_data_structure_element_get_by_xpath_raises_does_not_exist_error_if_not_found(
        self, mock_get
    ):
        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")

        mock_get.side_effect = exceptions.DoesNotExist("")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_element_api.get_by_xpath("value_xpath", mock_request)

    @patch.object(DataStructureElement, "get_by_xpath")
    def test_data_structure_element_get_by_xpath_return_data_if_found(self, mock_get):
        # Arrange
        mock_data_structure_element = DataStructureElement(
            tag="tag", value="value", options={"xpath.xml": "value_xpath"}
        )
        mock_get.return_value = mock_data_structure_element
        # Act
        result = DataStructureElement.get_by_xpath("value_xpath")
        # Assert
        self.assertEqual(result, mock_data_structure_element)


class TestDataStructureElementGetAllByChildId(TestCase):
    def test_data_structure_element_get_by_id_raises_model_error_if_not_found(self):
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.ModelError):
            data_structure_element_api.get_all_by_child_id(1, mock_request)

    @patch.object(DataStructureElement, "get_all_by_child_id")
    def test_data_structure_element_get_all_by_id_return_data_if_found(self, mock_get):
        # Arrange
        mock_data_structure_element = DataStructureElement(
            user="1", tag="tag", value="value"
        )
        mock_get.return_value = [mock_data_structure_element]
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")
        # Act
        result = data_structure_element_api.get_all_by_child_id(1, mock_request)
        # Assert
        self.assertTrue(all(isinstance(item, DataStructureElement) for item in result))


class TestDataStructureElementUpsert(TestCase):
    @patch.object(DataStructureElement, "save")
    def test_data_structure_element_upsert_return_data_structure_element(
        self, mock_save
    ):
        # Arrange
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = create_mock_user("1")

        mock_data_structure_element = DataStructureElement(
            user="1", tag="tag", value="value"
        )
        mock_save.return_value = mock_data_structure_element

        # Act
        result = data_structure_element_api.upsert(
            mock_data_structure_element, mock_request
        )

        # Assert
        self.assertIsInstance(result, DataStructureElement)
