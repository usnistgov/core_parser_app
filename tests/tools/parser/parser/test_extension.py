""" XSDParser tests for extension tag
"""
from os.path import join, dirname, abspath
from unittest.case import TestCase
from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE, SCHEMA_NAMESPACE
from xml_utils.xsd_tree.xsd_tree import XSDTree
from tests.test_utils import DataHandler
from core_parser_app.tools.parser.parser import XSDParser

# FIXME: use django finder
RESOURCES_PATH = join(dirname(abspath(__file__)), "..", "data")


class ParserCreateExtensionTestSuite(TestCase):
    """Parser Create Extension Test Suite"""

    def setUp(self):
        """Setup"""
        extension_data = join(RESOURCES_PATH, "parser", "extension")
        self.extension_data_handler = DataHandler(extension_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser
        self.parser = XSDParser()

    def test_generate_extension_with_multiple_children_returns_expected_json_dict(self):
        """test_generate_extension_with_multiple_children_returns_expected_json_dict"""
        xsd_files = join("multiple", "basic")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        result_dict = self.parser.generate_extension(
            xsd_element, xsd_tree, full_path="/root"
        )
        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(expected_dict, result_dict)

    def test_generate_extension_with_single_child_attribute_returns_expected_json_dict(
        self,
    ):
        """test_generate_extension_with_single_child_attribute_returns_expected_json_dict"""
        xsd_files = join("attribute", "single")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        result_dict = self.parser.generate_extension(
            xsd_element, xsd_tree, full_path="/root"
        )
        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(expected_dict, result_dict)

    def test_generate_extension_with_single_child_choice_returns_expected_json_dict(
        self,
    ):
        """test_generate_extension_with_single_child_choice_returns_expected_json_dict"""
        xsd_files = join("choice", "single")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        result_dict = self.parser.generate_extension(
            xsd_element, xsd_tree, full_path="/root"
        )
        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(expected_dict, result_dict)

    def test_generate_extension_with_single_child_sequence_returns_expected_json_dict(
        self,
    ):
        """test_generate_extension_with_single_child_sequence_returns_expected_json_dict"""
        xsd_files = join("sequence", "single")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        result_dict = self.parser.generate_extension(
            xsd_element, xsd_tree, full_path="/root"
        )
        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(expected_dict, result_dict)


class ParserReloadExtensionTestSuite(TestCase):
    """Parser Reload Extension Test Suite"""

    def setUp(self):
        """Setup"""
        # Init data path
        extension_data = join(RESOURCES_PATH, "parser", "extension")
        self.extension_data_handler = DataHandler(extension_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser with editing enabled
        self.parser = XSDParser()
        self.parser.editing = True

    def test_generate_extension_with_multiple_children_returns_expected_json_dict(self):
        """test_generate_extension_with_multiple_children_returns_expected_json_dict"""
        xsd_files = join("multiple", "basic")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_extension(
            xsd_element,
            xsd_tree,
            full_path="/root",
            edit_data_tree=edit_data_tree,
            default_value=edit_data_tree,
        )

        # Load expected dictionary and compare with result
        expected_dict = self.extension_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_generate_extension_with_single_child_attribute_returns_expected_json_dict(
        self,
    ):
        """test_generate_extension_with_single_child_attribute_returns_expected_json_dict"""
        xsd_files = join("attribute", "single")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_extension(
            xsd_element,
            xsd_tree,
            full_path="/root",
            edit_data_tree=edit_data_tree,
            default_value="entry0",
        )

        # Load expected dictionary and compare with result
        expected_dict = self.extension_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_generate_extension_with_single_child_choice_returns_expected_json_dict(
        self,
    ):
        """test_generate_extension_with_single_child_choice_returns_expected_json_dict"""
        xsd_files = join("choice", "single")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_extension(
            xsd_element, xsd_tree, full_path="/root", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.extension_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_generate_extension_with_single_child_sequence_returns_expected_json_dict(
        self,
    ):
        """test_generate_extension_with_single_child_sequence_returns_expected_json_dict"""
        xsd_files = join("sequence", "single")
        xsd_tree = self.extension_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_extension(
            xsd_element, xsd_tree, full_path="/root", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.extension_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)
