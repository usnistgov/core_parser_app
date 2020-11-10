""" Access control functions
"""
import logging

from django.contrib.auth.models import User
from django.http import HttpRequest
from mongoengine import QuerySet
from rest_framework.request import Request

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import CoreError

logger = logging.getLogger(__name__)


def _check_data_structure_elements_ownership(data_structure_element_list, user_id):
    """Check that the user is authorized to query or retrieve all
    DataStructureElement from the input list.

    Args:
        data_structure_element_list:
        user_id:

    Returns:
    """
    for data_structure_element in data_structure_element_list:
        if data_structure_element.user != user_id:
            raise AccessControlError("User is not the owner of the object.")


def get_accessible_owner(request):
    """Get a list of templates owners, the user can read from

    Args:
        request:

    Returns:

    """
    if request.user.is_anonymous:  # Non-existing user ID
        return "-1"
    elif request.user.is_superuser:  # No restrictions for superuser
        return None
    else:  # Logged in user
        return str(request.user.id)


def is_data_structure_element_owner(fn, *args, **kwargs):
    """Check that user is the owner of all input and output DataStructureElement.

    Args:
        fn:
        args:
        kwargs:

    Returns:
    """
    from core_parser_app.components.data_structure_element.models import (
        DataStructureElement,
    )

    if "request" in kwargs.keys() and (
        isinstance(kwargs["request"], HttpRequest)
        or isinstance(kwargs["request"], Request)
    ):
        request_user = kwargs["request"].user
    else:
        request = next(
            (
                arg
                for arg in args
                if isinstance(arg, HttpRequest) or isinstance(arg, Request)
            ),
            None,
        )
        request_user: User = request.user if request and request.user else None

    if request_user.is_superuser:  # Superusers bypass ACL
        return fn(*args, **kwargs)

    if request_user.is_anonymous:  # Anonymous users do not own anything
        raise AccessControlError("User is not the owner of the object.")

    # Check user has the right to query the input DataStructureElement list.
    _check_data_structure_elements_ownership(
        [arg for arg in args if isinstance(arg, DataStructureElement)]
        + [
            kwarg_value
            for kwarg_value in kwargs.values()
            if isinstance(kwarg_value, DataStructureElement)
        ],
        str(request_user.id),
    )

    # Run the function and add outputs to checklist
    fn_output = fn(*args, **kwargs)
    fn_output_data_structure_element_list = list()

    if isinstance(fn_output, DataStructureElement):
        fn_output_data_structure_element_list.append(fn_output)
    elif isinstance(fn_output, list) or isinstance(fn_output, QuerySet):
        output_data_structure_element_list = [
            out for out in fn_output if isinstance(out, DataStructureElement)
        ]

        # Check that all elements are DataStructureElement
        if len(fn_output) != len(output_data_structure_element_list):
            raise CoreError("Function returned unexpected elements")

        fn_output_data_structure_element_list += output_data_structure_element_list
    else:  # Outputs are neither a list nor an instance of DataStrctureElement
        raise CoreError("Function returned unexpected elements")

    # Check that the user is authorized to retrieve all outputs.
    _check_data_structure_elements_ownership(
        fn_output_data_structure_element_list,
        str(request_user.id),
    )

    return fn_output
