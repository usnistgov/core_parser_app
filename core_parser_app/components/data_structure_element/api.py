"""API for Data Structure Element
"""
from core_main_app.access_control.decorators import access_control
from core_parser_app import access_control as parser_access_control
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


@access_control(parser_access_control.is_data_structure_element_owner)
def upsert(data_structure_element, request):
    """Save or update the Data Structure Element

    Args:
        data_structure_element:
        request:

    Returns:

    """
    return data_structure_element.save()


@access_control(parser_access_control.is_data_structure_element_owner)
def get_all_by_child_id(child_id, request):
    """Get Data structure element object which contains the given child id in
    its children

    Args:
        child_id:
        request:

    Returns:

    """
    if request.user.is_superuser:
        return DataStructureElement.get_all_by_child_id(child_id)
    elif request.user.is_anonymous:
        return DataStructureElement.get_all_by_child_id_and_user(child_id, user=None)
    else:
        return DataStructureElement.get_all_by_child_id_and_user(
            child_id, user=str(request.user.id)
        )


@access_control(parser_access_control.is_data_structure_element_owner)
def get_by_id(data_structure_element_id, request):
    """Return DataStructureElement object with the given id

    Args:
        data_structure_element_id:
        request:

    Returns: DataStructureElement object
    """
    if request.user.is_superuser:
        return DataStructureElement.get_by_id(data_structure_element_id)
    elif request.user.is_anonymous:
        return DataStructureElement.get_by_id_and_user(
            data_structure_element_id, user=None
        )
    else:
        return DataStructureElement.get_by_id_and_user(
            data_structure_element_id, user=str(request.user.id)
        )


@access_control(parser_access_control.is_data_structure_element_owner)
def get_by_xpath(xpath, request):
    """List all DataStructureElement
    Args :
        xpath
    Returns: DataStructureElement collection
    """
    if request.user.is_superuser:
        return DataStructureElement.get_by_xpath(xpath)
    elif request.user.is_anonymous:
        return DataStructureElement.get_by_xpath_and_user(xpath, user=None)
    else:
        return DataStructureElement.get_by_xpath_and_user(
            xpath, user=str(request.user.id)
        )


@access_control(parser_access_control.is_data_structure_element_owner)
def remove_child(data_structure_element, child, request):
    """Remove child from existing DataStructureElement.

    Args:
        data_structure_element:
        child:
        request:

    Returns:

    """
    data_structure_element.update(pull__children=child)
    data_structure_element.reload()

    return data_structure_element


@access_control(parser_access_control.is_data_structure_element_owner)
def add_child(data_structure_element, child, request):
    """Add DataStrctureElement as a child to an existing DataStructureElement.

    Args:
        data_structure_element:
        child:
        request:

    Returns:

    """
    data_structure_element.update(add_to_set__children=[child])
    data_structure_element.reload()

    return data_structure_element


@access_control(parser_access_control.is_data_structure_element_owner)
def get_root_element(data_structure_element, request):
    """Return element's root.

    Args:
        data_structure_element:
        request:

    Returns:

    """
    current_element = data_structure_element
    parent_list = get_all_by_child_id(current_element.id, request)

    while len(parent_list) > 0:  # Browse parents while there is still one
        current_element = parent_list[0]
        parent_list = get_all_by_child_id(current_element.id, request)

    return current_element
