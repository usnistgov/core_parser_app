""" Data API
"""
from core_parser_app.components.data_structure_element.models import DataStructureElement


def upsert(data_structure_element):
    """ Save or update the Data Structure Element

    Args:
        data_structure_element:

    Returns:

    """
    return data_structure_element.save()


def get_all():
    """ List all DataStructureElement

        Returns: DataStructureElement collection
    """
    return DataStructureElement.get_all()


def get_all_by_child_id(child_id):
    """ Get Data structure element object which contains the given child id in its children

    Args:
        child_id:

    Returns:

    """
    return DataStructureElement.get_all_by_child_id(child_id)


def get_by_id(data_structure_element_id):
    """ Return DataStructureElement object with the given id

        Args:
            data_structure_element_id:

        Returns: DataStructureElement object
    """
    return DataStructureElement.get_by_id(data_structure_element_id)
