""" Access control functions
"""
import logging

from django.contrib.auth.models import Group, User
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from rest_framework.request import Request

import core_main_app.permissions.rights as rights
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import CoreError

logger = logging.getLogger(__name__)


def _check_data_structure_elements_access(data_structure_element_list, user):
    """Check that the user is authorized to query or retrieve all
    DataStructureElement from the input list.

    Args:
        data_structure_element_list:
        user:

    Returns:
    """
    for data_structure_element in data_structure_element_list:
        permission = data_structure_element.data_structure.get_object_permission()
        codename = permission.split(".")[1]
        # check if user can access this type of data structure element
        if user.is_anonymous:
            # Check in the ANONYMOUS_GROUP
            if not Group.objects.filter(
                Q(name=rights.ANONYMOUS_GROUP) & Q(permissions__codename=codename)
            ):
                raise AccessControlError(
                    "User does not have the permission to access this data structure."
                )
        elif not user.has_perm(permission):
            raise AccessControlError(
                "User does not have the permission to access this data structure."
            )
        # check if user is the owner
        _check_data_structure_element_ownership(data_structure_element, user)


def _check_data_structure_element_ownership(data_structure_element, user):
    """Check if the user is the owner

    Args:
        data_structure_element:
        user:

    Returns:

    """
    if data_structure_element.user and data_structure_element.user != str(user.id):
        raise AccessControlError("User is not the owner of the object.")


def is_data_structure_element_owner(fn, *args, **kwargs):
    """Check that user is the owner of all input and output DataStructureElement.

    Args:
        fn:
        args:
        kwargs:

    Returns:
    """
    from core_parser_app.components.data_structure.models import (
        DataStructureElement,
    )

    if "request" in kwargs.keys() and isinstance(
        kwargs["request"], (HttpRequest, Request)
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

    # Check user has the right to query the input DataStructureElement list.
    _check_data_structure_elements_access(
        [arg for arg in args if isinstance(arg, DataStructureElement)]
        + [
            kwarg_value
            for kwarg_value in kwargs.values()
            if isinstance(kwarg_value, DataStructureElement)
        ],
        request_user,
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
    _check_data_structure_elements_access(
        fn_output_data_structure_element_list,
        request_user,
    )

    return fn_output
