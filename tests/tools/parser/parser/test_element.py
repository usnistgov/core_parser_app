""" Tests for XSDParser - element
"""

from os.path import join, dirname, abspath

from django.test.testcases import TestCase

from core_parser_app.test_utils.utils import DataHandler
from core_parser_app.tools.parser.parser import XSDParser
from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE, SCHEMA_NAMESPACE

# FIXME: use django finder
RESOURCES_PATH = join(dirname(abspath(__file__)), '..', 'data')

# FIXME: tests about html content were removed
# FIXME: test reload data


class ParserGenerateElementTestSuite(TestCase):

    def setUp(self):
        element_data = join(RESOURCES_PATH, 'parser', 'element')
        self.element_data_handler = DataHandler(element_data)

        # set default namespace
        self.namespace = LXML_SCHEMA_NAMESPACE
        self.namespaces = {'xs': SCHEMA_NAMESPACE}

        # get an instance of the XSDParser
        self.parser = XSDParser()

    def test_create_simple_type_basic(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = self.element_data_handler.get_xsd(xsd_files)
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element',
                                     namespaces=self.namespaces)[0]

        # generate result dict
        result_dict = self.parser.generate_element(xsd_element, xsd_tree, full_path='')

        # load expected dictionary from files
        expected_dict = self.element_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_dict, expected_dict)

