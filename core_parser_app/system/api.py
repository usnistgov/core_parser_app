""" System APIs for the parser app
"""
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


# TODO: look into using delete cascade
# FIXME: not removing all data structure elements
def delete_branch_from_db(element_id):
    """Delete a branch from the database

    Args:
        element_id:

    Returns:
    """
    element = DataStructureElement.get_by_id(element_id, user=None)

    for child in element.children:
        delete_branch_from_db(str(child.pk))

    element.delete()
