""" Unit tests for `core_parser_app.tools.parser.XSDParser.generate_choice_extensions`
method.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_parser_app.tools.parser import parser
from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE


class TestGenerateChoiceExtensions(TestCase):
    """Unit tests for `generate_choice_extensions` method."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "xml_tree": MagicMock(),
            "choice_counter": None,
            "full_path": MagicMock(),
            "edit_data_tree": MagicMock(),
            "default_value": MagicMock(),
            "is_fixed": MagicMock(),
            "schema_location": MagicMock(),
        }

        self.mock_xsd_parser = parser.XSDParser()

    @patch.object(parser, "XSDTree")
    @patch.object(parser, "get_namespaces")
    @patch.object(parser, "get_target_namespace")
    @patch.object(parser.XSDParser, "generate_complex_type")
    def test_complex_type_calls_generate_complex_type(
        self,
        mock_generate_complex_type,
        mock_get_target_namespace,
        mock_get_namespaces,
        mock_xsd_tree,
    ):
        """test_complex_type_calls_generate_complex_type"""
        mock_complex_type_element = MagicMock()
        mock_complex_type_element.tag = f"{LXML_SCHEMA_NAMESPACE}complexType"
        self.mock_kwargs["element"] = [mock_complex_type_element]

        mock_get_target_namespace.return_value = (MagicMock(), MagicMock())

        self.mock_xsd_parser.generate_choice_extensions(**self.mock_kwargs)

        mock_generate_complex_type.assert_called()

    @patch.object(parser, "XSDTree")
    @patch.object(parser, "get_namespaces")
    @patch.object(parser, "get_target_namespace")
    @patch.object(parser.XSDParser, "generate_simple_type")
    def test_simple_type_calls_generate_simple_type(
        self,
        mock_generate_simple_type,
        mock_get_target_namespace,
        mock_get_namespaces,
        mock_xsd_tree,
    ):
        """test_simple_type_calls_generate_simple_type"""
        mock_simple_type_element = MagicMock()
        mock_simple_type_element.tag = f"{LXML_SCHEMA_NAMESPACE}simpleType"
        self.mock_kwargs["element"] = [mock_simple_type_element]

        mock_get_target_namespace.return_value = (MagicMock(), MagicMock())

        self.mock_xsd_parser.generate_choice_extensions(**self.mock_kwargs)

        mock_generate_simple_type.assert_called()
