""" Tests for XSDParser - element
"""
from os.path import join, dirname, abspath
from unittest.case import TestCase
from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE, SCHEMA_NAMESPACE
from xml_utils.xsd_tree.xsd_tree import XSDTree
from tests.test_utils import DataHandler
from core_parser_app.tools.parser.parser import XSDParser

# FIXME: use django finder
RESOURCES_PATH = join(dirname(abspath(__file__)), "..", "data")

# FIXME: tests about html content were removed


class ParserGenerateElementTestSuite(TestCase):
    """Parser Generate Element Test Suite"""

    def setUp(self):
        """setUp"""
        element_data = join(RESOURCES_PATH, "parser", "element")
        self.element_data_handler = DataHandler(element_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser
        self.parser = XSDParser()

    def test_create_simple_type_basic(self):
        """setUp"""
        xsd_files = join("simple_type", "basic")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element", namespaces=self.namespaces
        )[0]

        # Generate result dict
        result_dict = self.parser.generate_element(xsd_element, xsd_tree, full_path="")

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files)
        self.assertDictEqual(expected_dict, result_dict)

    def test_create_simple_type_basic_ns(self):
        """setUp"""
        xsd_files = join("simple_type", "basic_ns")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element", namespaces=self.namespaces
        )[0]

        # Generate result dict
        result_dict = self.parser.generate_element(xsd_element, xsd_tree, full_path="")

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files)
        self.assertDictEqual(expected_dict, result_dict)

    def test_create_simple_type_unbounded(self):
        """setUp"""
        xsd_files = join("simple_type", "unbounded")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence/xs:element",
            namespaces=self.namespaces,
        )[0]

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="/ex:root[1]"
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files)
        self.assertDictEqual(expected_dict, result_dict)

    def test_create_simple_type_unbounded_ns(self):
        """setUp"""
        xsd_files = join("simple_type", "unbounded_ns")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence/xs:element",
            namespaces=self.namespaces,
        )[0]

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="/root[1]"
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files)
        self.assertDictEqual(expected_dict, result_dict)

    def test_create_complex_type_basic(self):
        """setUp"""
        xsd_files = join("complex_type", "basic")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element", namespaces=self.namespaces
        )[0]

        # generate result dict
        result_dict = self.parser.generate_element(xsd_element, xsd_tree, full_path="")

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files)
        self.assertDictEqual(expected_dict, result_dict)

    def test_create_complex_type_unbounded(self):
        """setUp"""
        xsd_files = join("complex_type", "unbounded")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence/xs:element",
            namespaces=self.namespaces,
        )[0]

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="/root"
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files)
        self.assertDictEqual(expected_dict, result_dict)


class ParserReloadElementTestSuite(TestCase):
    """Parser Reload Element Test Suite"""

    def setUp(self):
        """setUp"""
        # Init data path
        element_data = join(RESOURCES_PATH, "parser", "element")
        self.element_data_handler = DataHandler(element_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser with editing enabled
        self.parser = XSDParser()
        self.parser.editing = True

    def test_reload_simple_type_basic(self):
        """test_reload_simple_type_basic"""
        xsd_files = join("simple_type", "basic")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element", namespaces=self.namespaces
        )[0]

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_reload_simple_type_basic_ns(self):
        """test_reload_simple_type_basic_ns"""
        xsd_files = join("simple_type", "basic_ns")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element", namespaces=self.namespaces
        )[0]

        xml_tree = self.element_data_handler.get_xml(xsd_files.replace("_ns", ""))
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_reload_simple_type_unbounded(self):
        """test_reload_simple_type_unbounded"""
        xsd_files = join("simple_type", "unbounded")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence/xs:element",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element,
            xsd_tree,
            full_path="/ex:root[1]",
            edit_data_tree=edit_data_tree,
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_reload_simple_type_unbounded_ns(self):
        """test_reload_simple_type_unbounded_ns"""
        xsd_files = join("simple_type", "unbounded_ns")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence/xs:element",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="/root[1]", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_reload_complex_type_basic(self):
        """test_reload_complex_type_basic"""
        xsd_files = join("complex_type", "basic")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:element", namespaces=self.namespaces
        )[0]

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)

    def test_create_complex_type_unbounded(self):
        """test_create_complex_type_unbounded"""
        xsd_files = join("complex_type", "unbounded")
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence/xs:element",
            namespaces=self.namespaces,
        )[0]

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_element(
            xsd_element, xsd_tree, full_path="/root", edit_data_tree=edit_data_tree
        )

        # Load expected dictionary and compare with result
        expected_dict = self.element_data_handler.get_json(xsd_files + ".reload")
        self.assertDictEqual(expected_dict, result_dict)
