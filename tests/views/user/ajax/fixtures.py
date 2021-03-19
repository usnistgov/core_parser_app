""" Fixtures for user-side AJAX
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)
from tests.fixtures_utils import MockDataStructure


class DataStructureElementFixture(FixtureInterface):
    data_structure = None
    data_structure_element_root = None
    data_structure_element_child = None

    def insert_data(self, user="1"):
        self.generate_data_structure_element(user)

    def generate_data_structure_element(self, user):
        self.data_structure = MockDataStructure(
            user="1", template="template", name="name"
        ).save()
        self.data_structure_element_child = DataStructureElement(
            user=user, tag="child", value="value", data_structure=self.data_structure
        )
        self.data_structure_element_child.save()

        self.data_structure_element_root = DataStructureElement(
            user=user,
            tag="root",
            children=[self.data_structure_element_child.id],
            data_structure=self.data_structure,
        )
        self.data_structure_element_root.save()
