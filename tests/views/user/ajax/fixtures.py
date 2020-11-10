""" Fixtures for user-side AJAX
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_parser_app.components.data_structure.models import DataStructure
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


class MockDataStructure(DataStructure):
    pass


class DataStructureElementFixture(FixtureInterface):
    data_structure = None
    data_structure_element_root = None
    data_structure_element_child = None

    def insert_data(self):
        self.generate_data_structure_element()

    def generate_data_structure_element(self):
        self.data_structure_element_child = DataStructureElement(
            user="1", tag="child", value="value"
        )
        self.data_structure_element_child.save()

        self.data_structure_element_root = DataStructureElement(
            user="1", tag="root", children=[self.data_structure_element_child.id]
        )
        self.data_structure_element_root.save()
