""" Fixtures for user-side AJAX
"""
from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from tests.fixtures_utils import MockDataStructure


class DataStructureElementFixture(FixtureInterface):
    """Data Structure Element Fixture"""

    template = None
    data_structure = None
    data_structure_element_root = None
    data_structure_element_child = None

    def insert_data(self, user="1"):
        """insert_data

        Args:
            user:
        """

        self.generate_template()
        self.generate_data_structure_element(user)

    def generate_template(self):
        """generate_template"""

        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template = Template(
            content=xsd,
            hash="hash",
            filename="template.xsd",
            user=None,
            _cls="Template",
        )
        self.template.save()

    def generate_data_structure_element(self, user):
        """insert_data

        Args:
            user:
        """
        self.data_structure = MockDataStructure(
            user="1", template=self.template, name="name"
        )
        self.data_structure.save()

        self.data_structure_element_root = DataStructureElement(
            user=user,
            tag="root",
            data_structure=self.data_structure,
        )
        self.data_structure_element_root.save()
        self.data_structure_element_child = DataStructureElement(
            user=user,
            tag="child",
            value="value",
            data_structure=self.data_structure,
            parent=self.data_structure_element_root,
        )
        self.data_structure_element_child.save()
