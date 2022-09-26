""" XSDParser tests for restriction tag
"""
from os.path import join, dirname, abspath

from django.test.testcases import TestCase

from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE, SCHEMA_NAMESPACE
from xml_utils.xsd_tree.xsd_tree import XSDTree
from tests.test_utils import DataHandler
from core_parser_app.tools.parser.parser import XSDParser

RESOURCES_PATH = join(dirname(abspath(__file__)), "..", "data")


class ParserCreateSequenceTestSuite(TestCase):
    """Test creation of elements under sequence"""

    def setUp(self):
        """Setup"""
        sequence_data = join(RESOURCES_PATH, "parser", "sequence")
        self.sequence_data_handler = DataHandler(sequence_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser
        self.parser = XSDParser()

    def _run_test(self, xsd_files):
        """Run test

        Args:
            xsd_files:

        Returns:
        """

        xsd_xpath = "/xs:schema/xs:complexType/xs:sequence"

        xsd_tree = self.sequence_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(xsd_xpath, namespaces=self.namespaces)[0]

        result_dict = self.parser.generate_sequence(
            xsd_element, xsd_tree, full_path="/root"
        )

        expected_dict = self.sequence_data_handler.get_json(xsd_files)

        return result_dict, expected_dict

    def test_create_element_basic(self):
        """test_create_element_basic"""

        xsd_files = join("element", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_element_unbounded(self):
        """test_create_element_unbounded"""
        xsd_files = join("element", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_choice_basic(self):
        """test_create_element_unbounded"""
        xsd_files = join("choice", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_choice_unbounded(self):
        """test_create_element_unbounded"""
        xsd_files = join("choice", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_sequence_basic(self):
        """test_create_sequence_basic"""
        xsd_files = join("sequence", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_sequence_unbounded(self):
        """test_create_sequence_unbounded"""
        xsd_files = join("sequence", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_multiple_basic(self):
        """test_create_multiple_basic"""
        xsd_files = join("multiple", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_create_multiple_unbounded(self):
        """test_create_multiple_unbounded"""
        xsd_files = join("multiple", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)


class ParserReloadSequenceTestSuite(TestCase):
    """Parser Reload Sequence Test Suite"""

    maxDiff = None

    def setUp(self):
        """Setup"""
        # Init data path
        sequence_data = join(RESOURCES_PATH, "parser", "sequence")
        self.sequence_data_handler = DataHandler(sequence_data)

        # Set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {"xs": SCHEMA_NAMESPACE}

        # Get an instance of the XSDParser with editing enabled
        self.parser = XSDParser()
        self.parser.editing = True

    def _run_test(self, xsd_files):
        """Run test

        Args:
            xsd_files:

        Returns:
        """
        xsd_tree = self.sequence_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath(
            "/xs:schema/xs:complexType/xs:sequence", namespaces=self.namespaces
        )[0]

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = XSDTree.tostring(xml_tree)
        edit_data_tree = XSDTree.transform_to_xml(xml_data)

        # Generate result dict
        result_dict = self.parser.generate_sequence(
            xsd_element,
            xsd_tree,
            full_path="/root",
            edit_data_tree=edit_data_tree,
        )

        # Load expected dictionary and compare with result
        expected_dict = self.sequence_data_handler.get_json(
            xsd_files + ".reload"
        )

        return result_dict, expected_dict

    def test_reload_element_basic(self):
        """test_create_multiple_basic"""
        xsd_files = join("element", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_element_unbounded(self):
        """test_create_multiple_basic"""
        # fixme correct bug
        xsd_files = join("element", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_choice_basic(self):
        """test_reload_choice_basic"""
        xsd_files = join("choice", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_choice_unbounded(self):
        """test_reload_choice_unbounded"""
        xsd_files = join("choice", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_sequence_basic(self):
        """test_reload_sequence_basic"""
        xsd_files = join("sequence", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_sequence_unbounded(self):
        """test_reload_sequence_unbounded"""
        xsd_files = join("sequence", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_multiple_basic(self):
        """test_reload_multiple_basic"""
        xsd_files = join("multiple", "basic")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

    def test_reload_multiple_unbounded(self):
        """test_reload_multiple_unbounded"""
        xsd_files = join("multiple", "unbounded")
        result_dict, expected_dict = self._run_test(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)
