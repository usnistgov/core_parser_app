""" Tests for XSDParser - complex content
"""
from os.path import join, dirname, abspath
from unittest.case import TestCase

from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE, SCHEMA_NAMESPACE
from xml_utils.xsd_tree.xsd_tree import XSDTree
from tests.test_utils import DataHandler
from core_parser_app.tools.parser.parser import XSDParser

# FIXME: use django finder
RESOURCES_PATH = join(dirname(abspath(__file__)), "..", "data")


class ParserCreateComplexContentTestSuite(TestCase):
    """Parser Create Complex Content Test Suite"""

    maxDiff = None

    def setUp(self):
        """setUp"""
        """ setUp """
        # Setup data handler
        complex_content_data = join(
            RESOURCES_PATH, "parser", "complex_content"
        )
        self.complex_content_data_handler = DataHandler(complex_content_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser
        self.parser = XSDParser()

    def test_create_extension_basic(self):
        """test_create_extension_basic"""
        xsd_files = join("extension", "basic")
        xsd_tree = self.complex_content_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent",
            namespaces=self.namespaces,
        )[0]

        result_string = self.parser.generate_complex_content(
            xsd_element, xsd_tree, full_path="/root"
        )

        expected_dict = self.complex_content_data_handler.get_json(xsd_files)
        self.assertDictEqual(result_string, expected_dict)

    def test_create_restriction_basic(self):
        """test_create_restriction_basic"""
        xsd_files = join("restriction", "basic")
        xsd_tree = self.complex_content_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent",
            namespaces=self.namespaces,
        )[0]

        # Generate result dict
        result_string = self.parser.generate_complex_content(
            xsd_element, xsd_tree, full_path="/root"
        )

        # Load expected dictionary and compare with result
        expected_dict = self.complex_content_data_handler.get_json(xsd_files)
        self.assertDictEqual(result_string, expected_dict)


class ParserReloadComplexContentTestSuite(TestCase):
    """Parser Reload Complex Content Test Suite"""

    maxDiff = None

    def setUp(self):
        """setUp"""
        complex_content_data = join(
            RESOURCES_PATH, "parser", "complex_content"
        )
        self.complex_content_data_handler = DataHandler(complex_content_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser
        self.parser = XSDParser()
        self.parser.editing = True

    def test_reload_extension_basic(self):
        """test_reload_extension_basic"""
        xsd_files = join("extension", "basic")
        xsd_tree = self.complex_content_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.complex_content_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_string = self.parser.generate_complex_content(
            xsd_element,
            xsd_tree,
            full_path="/root",
            edit_data_tree=edit_data_tree,
        )

        # Load expected dictionary and compare with result
        expected_dict = self.complex_content_data_handler.get_json(
            f"{xsd_files}.reload"
        )
        self.assertDictEqual(result_string, expected_dict)

    def test_reload_restriction_basic(self):
        """test_reload_restriction_basic"""
        xsd_files = join("restriction", "basic")
        xsd_tree = self.complex_content_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.complex_content_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_string = self.parser.generate_complex_content(
            xsd_element,
            xsd_tree,
            full_path="/root",
            edit_data_tree=edit_data_tree,
        )

        # Load expected dictionary and compare with result
        expected_dict = self.complex_content_data_handler.get_json(
            f"{xsd_files}.reload"
        )
        self.assertDictEqual(result_string, expected_dict)
