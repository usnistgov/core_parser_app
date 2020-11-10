""" Fixtures file for Data Structure Element
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


class DataStructureElementFixtures(FixtureInterface):
    """Represents Data structure element fixtures"""

    def __init__(self):
        self.default_user_id = "1"
        self.data_structure_element_collection = None

    def insert_data(self):
        """Insert a set of Data

        Returns:
        """
        self.generate_data_structure_elements()

    def generate_data_structure_element(
        self, element_id, user=None, options=None, children=None
    ):
        """Return a DataStructureElement with the given parameters

        Args:
            element_id:
            children:

        Returns:
        """
        children = [] if children is None else children
        options = {} if options is None else options
        user = self.default_user_id if user is None else user

        return DataStructureElement(
            user=user,
            tag="tag_%s" % element_id,
            value="value_%s" % element_id,
            options=options,
            children=children,
        ).save()

    def generate_data_structure_elements(self):
        """Insert data structure elements on multiple levels in mock database

        Example:

            Root -> 1000 -> 1100 -> 1110
                                 -> 1120 -> 1121
                         -> 1200
                 -> 2000

        Returns:

        """
        element_1121 = self.generate_data_structure_element(
            "1121", options={"xpath": {"xml": "value_xpath"}}
        )
        element_1120 = self.generate_data_structure_element(
            "1120", children=[element_1121]
        )
        element_1110 = self.generate_data_structure_element("1110")
        element_1100 = self.generate_data_structure_element(
            "1100", children=[element_1110, element_1120]
        )
        element_1200 = self.generate_data_structure_element("1200")
        element_1000 = self.generate_data_structure_element(
            "1000", children=[element_1100, element_1200]
        )
        element_2000 = self.generate_data_structure_element("2000")
        element_root = self.generate_data_structure_element(
            "root", children=[element_1000, element_2000]
        )

        # Set the collection of data structure element
        self.data_structure_element_collection = {
            "root": element_root,
            "1000": element_1000,
            "1100": element_1100,
            "1110": element_1110,
            "1120": element_1120,
            "1121": element_1121,
            "1200": element_1200,
            "2000": element_2000,
        }
