""" XSDParser tests for restriction tag
"""
from os.path import join, dirname, abspath
from unittest.case import TestCase

from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE, SCHEMA_NAMESPACE
from xml_utils.xsd_tree.xsd_tree import XSDTree
from core_parser_app.tools.parser.parser import XSDParser
from tests.test_utils import DataHandler

RESOURCES_PATH = join(dirname(abspath(__file__)), "..", "data")


class ParserCreateRestrictionTestSuite(TestCase):
    """Parser Create Restriction Test Suite"""

    def setUp(self):
        """setUp"""

        restriction_data = join(RESOURCES_PATH, "parser", "restriction")
        self.restriction_data_handler = DataHandler(restriction_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser
        self.parser = XSDParser()

    def _run_test(self, xsd_files):
        xsd_tree = self.restriction_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:simpleType/xs:restriction", namespaces=self.namespaces
        )[0]

        result_dict = self.parser.generate_restriction(
            xsd_element, xsd_tree, full_path="/root"
        )
        expected_dict = self.restriction_data_handler.get_json(xsd_files)

        return result_dict, expected_dict

    def test_enumeration(self):
        """test_enumeration"""

        xsd_files = join("enumeration", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)
        self.assertDictEqual(result_dict, expected_dict)

    def test_simple_type(self):
        """test_simple_type"""
        xsd_files = join("simple_type", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)


class ParserReloadRestrictionTestSuite(TestCase):
    """Parser Reload Restriction Test Suite"""

    def setUp(self):
        """setUp"""

        # Init data path
        retriction_data = join(RESOURCES_PATH, "parser", "restriction")
        self.restriction_data_handler = DataHandler(retriction_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser with editing enabled
        self.parser = XSDParser()
        self.parser.editing = True

    def _run_test(self, xsd_files):
        xsd_tree = self.restriction_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:simpleType/xs:restriction", namespaces=self.namespaces
        )[0]

        xml_tree = self.restriction_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_restriction(
            xsd_element,
            xsd_tree,
            full_path="/root",
            edit_data_tree=edit_data_tree,
            default_value=edit_data_tree.text,
        )

        # Load expected dictionary and compare with result
        expected_dict = self.restriction_data_handler.get_json(xsd_files + ".reload")

        return result_dict, expected_dict

    def test_enumeration(self):
        """test_enumeration"""

        xsd_files = join("enumeration", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(expected_dict, result_dict)

    def test_simple_type(self):
        """test_simple_type"""

        xsd_files = join("simple_type", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(expected_dict, result_dict)
