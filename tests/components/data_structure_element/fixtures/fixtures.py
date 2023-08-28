""" Fixtures file for Data Structure Element
"""
from django.contrib.auth.models import User, Group, Permission

from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from tests import rights
from tests.fixtures_utils import MockDataStructure, create_user


class DataStructureElementFixtures(FixtureInterface):
    """Represents Data structure element fixtures"""

    def __init__(self, add_user_perm=True, add_anon_perm=True):
        """

        Args:
            add_user_perm:
            add_anon_perm:
        """
        # delete all users
        User.objects.all().delete()
        Group.objects.all().delete()
        # Create new users
        self.staff_user = create_user(username="staff", is_staff=True)
        self.superuser = create_user(username="superuser", is_superuser=True)
        self.default_owner_with_perm = create_user(username="user1")
        self.other_user_with_perm = create_user(username="user2")
        self.user_without_perm = create_user(username="user3")
        self.default_user_id = str(self.default_owner_with_perm.id)
        self.data_structure = None
        self.data_structure_element_collection = None
        self.template = None

        if add_user_perm:
            default_group, created = Group.objects.get_or_create(
                name="default"
            )
            mock_data_structure_access_perm = Permission.objects.get(
                codename=rights.MOCK_DATA_STRUCTURE_ACCESS
            )
            default_group.permissions.add(mock_data_structure_access_perm)
            default_group.user_set.add(self.default_owner_with_perm)
            default_group.user_set.add(self.other_user_with_perm)
        if add_anon_perm:
            anonymous_group, created = Group.objects.get_or_create(
                name="anonymous"
            )

            mock_anon_data_structure_access_perm = Permission.objects.get(
                codename=rights.MOCK_ANON_DATA_STRUCTURE_ACCESS
            )
            anonymous_group.permissions.add(
                mock_anon_data_structure_access_perm
            )

    def insert_data(self, user=None, data_structure_class=MockDataStructure):
        """Insert a set of Data
            user: owner

        Returns:
        """
        if not user:
            user = self.default_owner_with_perm
        self.generate_template()
        self.generate_data_structure(
            user=user, data_structure_class=data_structure_class
        )
        self.generate_data_structure_elements(user=user)

    def generate_template(self):
        """generate_template

        Returns:
        """
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template = Template(
            content=xsd,
            _hash="hash",
            filename="template.xsd",
            user=None,
            _cls="Template",
        )
        self.template.save()

    def generate_data_structure(self, user, data_structure_class):
        """generate_template

        Args:
            user:
            data_structure_class:

        Returns:
        """
        self.data_structure = data_structure_class(
            user=str(user.id), template=self.template, name="name"
        )
        self.data_structure.save()

    def _generate_data_structure_element(
        self,
        element_id,
        user=None,
        options=None,
        parent=None,
        data_structure=None,
    ):
        """Return a DataStructureElement with the given parameters

        Args:
            element_id:
            user:
            options:
            parent:
            data_structure:

        Returns:
        """
        options = {} if options is None else options
        user = self.default_user_id if not user else str(user.id)

        data_structure_element = DataStructureElement(
            user=user,
            tag=f"tag_{element_id}",
            value=f"value_{element_id}",
            options=options,
            parent=parent,
            data_structure=data_structure,
        )
        data_structure_element.save()
        return data_structure_element

    def generate_data_structure_elements(self, user=None):
        """Insert data structure elements on multiple levels in mock database

        Example:

            Root -> 1000 -> 1100 -> 1110
                                 -> 1120 -> 1121
                         -> 1200
                 -> 2000

        Returns:

        """
        element_root = self._generate_data_structure_element(
            "root",
            user=user,
            data_structure=self.data_structure,
        )
        element_1000 = self._generate_data_structure_element(
            "1000",
            user=user,
            data_structure=self.data_structure,
        )
        element_2000 = self._generate_data_structure_element(
            "2000", user=user, data_structure=self.data_structure
        )
        element_1100 = self._generate_data_structure_element(
            "1100",
            user=user,
            parent=element_1000,
            data_structure=self.data_structure,
        )
        element_1200 = self._generate_data_structure_element(
            "1200",
            user=user,
            parent=element_1000,
            data_structure=self.data_structure,
        )

        element_1110 = self._generate_data_structure_element(
            "1110",
            user=user,
            parent=element_1100,
            data_structure=self.data_structure,
        )

        element_1120 = self._generate_data_structure_element(
            "1120",
            user=user,
            parent=element_1100,
            data_structure=self.data_structure,
        )

        element_1121 = self._generate_data_structure_element(
            "1121",
            user=user,
            options={"xpath": {"xml": "value_xpath"}},
            parent=element_1120,
            data_structure=self.data_structure,
        )
        self.data_structure.data_structure_element_root = element_root
        self.data_structure.save()

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
