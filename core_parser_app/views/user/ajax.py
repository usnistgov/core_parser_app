"""AJAX views
"""
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from django.http.response import HttpResponseBadRequest, HttpResponse
import json


def get_data_structure_element_value(request):
    """Gets the value of a data structure element

    Args:
        request:

    Returns:

    """
    if 'id' not in request.POST:
        return HttpResponseBadRequest()

    element = data_structure_element_api.get_by_id(request.POST['id'])
    element_value = element.value

    if element.tag == 'module':
        element_value = {
            'data': element.options['data'],
            'attributes': element.options['attributes']
        }

    return HttpResponse(json.dumps({'value': element_value}), content_type='application/json')
