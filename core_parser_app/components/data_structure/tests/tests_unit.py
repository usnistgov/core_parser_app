""" Unit Test Data Structure Element
"""
import core_parser_app.components.data_structure.api as data_structure_api
from core_parser_app.components.data_structure.models import DataStructure
from core_main_app.components.template.models import Template
from core_main_app.commons import exceptions
from unittest.case import TestCase
from mock import patch


class TestDataStructureGetAll(TestCase):

    @patch.object(DataStructure, 'get_all')
    def test_data_get_all_return_collection_of_data(self, mock_list):
        # Arrange
        mock_data_1 = DataStructure('1', _get_template(), 'name_title_1')
        mock_data_2 = DataStructure('1', _get_template(), 'name_title_2')
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_structure_api.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, DataStructure) for item in result))


class TestDataStructureGetById(TestCase):

    @patch.object(DataStructure, 'get_by_id')
    def test_data_structure_get_by_id_raises_does_not_exist_error_if_not_found(self, mock_get):
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist('')
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_api.get_by_id(1)

    def test_data_structure_get_by_id_raises_model_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.ModelError):
            data_structure_api.get_by_id(1)

    @patch.object(DataStructure, 'get_by_id')
    def test_data_structure_get_by_id_return_data_if_found(self, mock_get):
        # Arrange
        mock_data_structure = DataStructure("1", Template(), "name")
        mock_get.return_value = mock_data_structure
        # Act
        result = data_structure_api.get_by_id(1)
        # Assert
        self.assertIsInstance(result, DataStructure)


class TestDataStructureUpsert(TestCase):

    @patch.object(DataStructure, 'save')
    def test_data_structure_upsert_return_data_structure_element(self, mock_save):
        # Arrange
        mock_data_structure = DataStructure("1", Template(), "name")
        mock_save.return_value = mock_data_structure
        # Act
        result = data_structure_api.upsert(mock_data_structure)
        # Assert
        self.assertIsInstance(result, DataStructure)


class TestDataStructureGetByUserIdAndTemplateId(TestCase):

    @patch.object(DataStructure, 'get_by_user_id_and_template_id')
    def test_data_structure_get_by_user_and_template_return_collection_of_data_structure(self, mock_list):
        # Arrange
        mock_data_1 = DataStructure('1', _get_template(), 'name_title_1')
        mock_data_2 = DataStructure('1', _get_template(), 'name_title_2')
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_structure_api.get_by_user_id_and_template_id(1, 1)
        # Assert
        self.assertTrue(all(isinstance(item, DataStructure) for item in result))


def _get_template():
    template = Template()
    template.id_field = 1
    xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
          '<xs:element name="tag"></xs:element></xs:schema>'
    template.content = xsd
    return template
