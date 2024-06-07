""" System APIs for the parser app
"""


def delete_branch_from_db(element_id):
    """Delete a branch from the database
    Args:
        element_id:
    Returns:
    """
    from core_parser_app.components.data_structure.models import (
        DataStructureElement,
    )

    element = DataStructureElement.get_by_id(element_id)
    for child in element.children.all():
        delete_branch_from_db(str(child.pk))
    element.delete()


def get_data_structure_by_id(data_structure_id):
    """get_data_structure_by_id
    Args:
        data_structure_id:
    Returns:
    """
    from core_parser_app.components.data_structure.models import (
        DataStructure,
    )

    return DataStructure.get_by_id(data_structure_id)
