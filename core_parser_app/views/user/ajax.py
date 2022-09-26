"""AJAX views
"""
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)


@login_required
def data_structure_element_value(request):
    """Endpoint for data structure element value

    Args:
        request:

    Returns:

    """
    if request.method == "GET":
        return get_data_structure_element_value(request)
    elif request.method == "POST":
        return save_data_structure_element_value(request)


def get_data_structure_element_value(request):
    """Gets the value of a data structure element

    Args:
        request:

    Returns:

    """
    if "id" not in request.GET:
        return HttpResponseBadRequest()

    try:
        element = data_structure_element_api.get_by_id(
            request.GET["id"], request
        )
        element_value = element.value

        if element.tag == "module":
            element_value = {
                "data": element.options["data"],
                "attributes": element.options["attributes"],
            }

        return HttpResponse(
            json.dumps({"value": element_value}),
            content_type="application/json",
        )
    except (AccessControlError, DoesNotExist) as exc:
        return HttpResponseBadRequest(json.dumps({"message": str(exc)}))


def save_data_structure_element_value(request):
    """Saves the value of a data structure element

    Args:
        request:

    Returns:

    """
    if "id" not in request.POST or "value" not in request.POST:
        return HttpResponseBadRequest(
            "Error when trying to data structure element: id or value is missing."
        )

    try:
        input_element = data_structure_element_api.get_by_id(
            request.POST["id"], request
        )

        input_previous_value = input_element.value
        input_element.value = request.POST["value"]
        data_structure_element_api.upsert(input_element, request)

        return HttpResponse(
            json.dumps({"replaced": input_previous_value}),
            content_type="application/json",
        )
    except (AccessControlError, DoesNotExist) as exc:
        return HttpResponseBadRequest(json.dumps({"message": str(exc)}))
