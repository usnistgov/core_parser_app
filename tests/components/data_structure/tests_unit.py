""" Unit Test Data Structure
"""
from unittest.case import TestCase
from unittest.mock import patch

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
import core_parser_app.components.data_structure.api as data_structure_api
from core_parser_app.components.data_structure.models import (
    DataStructure,
)


class TestDataStructureGetById(TestCase):
    """Test Data Structure Get By Id"""

    @patch.object(DataStructure, "get_by_id")
    def test_data_structure_get_by_id_raises_does_not_exist_error_if_not_found(
        self, mock_get
    ):
        """test_data_structure_get_by_id_raises_does_not_exist_error_if_not_found"""

        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_api.get_by_id(-1)

    @patch.object(DataStructure, "get_by_id")
    def test_data_structure_get_by_id_return_data_if_found(self, mock_get):
        """test_data_structure_get_by_id_return_data_if_found"""

        # Arrange
        mock_get.return_value = _get_data_structure()

        # Act
        result = data_structure_api.get_by_id(1)
        # Assert
        self.assertIsInstance(result, DataStructure)


def _get_data_structure():

    template = Template()
    template.id_field = 1
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd

    return DataStructure(user="1", template=template, name="name_title_2")
