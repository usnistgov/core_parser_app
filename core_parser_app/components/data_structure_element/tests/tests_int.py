""" Integration test of Data structure element
"""
from core_parser_app.components.data_structure_element.models import DataStructureElement
from core_parser_app.components.data_structure_element.tests.fixtures.fixtures import DataFixtures
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from core_main_app.commons import exceptions
from bson.objectid import ObjectId

fixture_data = DataFixtures()


class TestDataStructureElementGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_structure_element_get_all_return_collection_of_data(self):
        # Act
        result = DataStructureElement.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, DataStructureElement) for item in result))

    def test_data_structure_element_get_all_return_all_data_structure_element_in_collection(self):
        # Act
        result = DataStructureElement.get_all()
        # Assert
        self.assertTrue(len(self.fixture.data_structure_element_collection) == len(result))


class TestDataStructureElementGetById(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_by_id_raises_does_not_exist_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            DataStructureElement.get_by_id(ObjectId())

    def test_data_get_by_id_return_data_if_found(self):
        # Act
        result = DataStructureElement.get_by_id(self.fixture.data_structure_element_collection[1].id)
        # Assert
        self.assertEqual(result, self.fixture.data_structure_element_collection[1])

    def test_data_get_by_id_raises_exception_if_fail(self):
        # Act # Assert
        with self.assertRaises(Exception):
            DataStructureElement.get_by_id("")


class TestDataStructureElementGetByChildId(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_structure_element_get_by_child_id(self):
        # Act
        result = DataStructureElement.get_all_by_child_id(self.fixture.data_structure_element_child_id_1)
        # Assert
        self.assertTrue(all(isinstance(item, DataStructureElement) for item in result))

    def test_data_get_by_child_id_raises_exception_if_fail(self):
        # Act # Assert
        with self.assertRaises(Exception):
            DataStructureElement.get_all_by_child_id("")



