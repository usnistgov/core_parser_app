""" Tests for Parser
"""
from unittest.mock import patch

from django.test.testcases import TestCase

from core_parser_app.tools.parser.exceptions import ParserError
from core_parser_app.tools.parser.parser import XSDParser


class TestGenerateForm(TestCase):
    """Test generate form"""

    @patch.object(XSDParser, "generate_element")
    def test_generate_form_raises_parser_error(self, mock_generate_element):
        """

        Args:
            mock_generate_element:

        Returns:

        """
        # Arrange
        mock_generate_element.side_effect = ParserError("error")
        parser = XSDParser()
        with self.assertRaises(ParserError):
            parser.generate_form(
                xsd_doc_data="<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
                "<xs:element name='root'/>"
                "</xs:schema>"
            )
