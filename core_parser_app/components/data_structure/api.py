""" Data API
"""
from core_parser_app.components.data_structure.models import DataStructure


def upsert(data_structure):
    """ Save or update the Data Structure Element

    Args:
        data_structure:

    Returns:

    """
    return data_structure.save()


def get_by_id(data_structure_id):
    """ Return DataStructureElement object with the given id

        Args:
            data_structure_id:

        Returns: DataStructureElement object
    """
    return DataStructure.get_by_id(data_structure_id)
