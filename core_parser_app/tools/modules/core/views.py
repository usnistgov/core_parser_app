"""Core modules views
"""
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from core_parser_app.tools.modules.core.models import AutoKeyRefModule, BlobHostModule, RemoteBlobHostModule, \
    AdvancedBlobHostModule

from django.http.response import HttpResponse
import json


def blob_host(request):
    """ BLOB host module view

    Args:
        request:

    Returns:

    """
    return BlobHostModule().render(request)


def remote_blob_host(request):
    """ Remote BLOB host view

    Args:
        request:

    Returns:

    """
    return RemoteBlobHostModule().render(request)


def advanced_blob_host(request):
    """ Advanced BLOB host view

    Args:
        request:

    Returns:

    """
    return AdvancedBlobHostModule().render(request)


def auto_keyref(request):
    """

    Args:
        request:

    Returns:

    """
    return AutoKeyRefModule().render(request)


def get_updated_keys(request):
    """
        updated_keys[key] = {'ids': [],
                            'tagIDs': []}
        key = key name
        ids = list of possible values for a key
        tagIDs = HTML element that needs to be updated with the values (keyrefs)
    """

    # delete keys that have been deleted
    for key, values in request.session['keys'].iteritems():
        deleted_ids = []
        for module_id in values['module_ids']:
            try:
                data_structure_element_api.get_by_id(module_id)
            except Exception:
                deleted_ids.append(module_id)
        request.session['keys'][key]['module_ids'] = [item for item in request.session['keys'][key]['module_ids']
                                                if item not in deleted_ids]
    # delete keyrefs that have been deleted
    for keyref, values in request.session['keyrefs'].iteritems():
        deleted_ids = []
        for module_id in values['module_ids']:
            try:
                data_structure_element_api.get_by_id(module_id)
            except Exception:
                deleted_ids.append(module_id)
        request.session['keyrefs'][keyref]['module_ids'] = [item for item in request.session['keyrefs'][keyref]['module_ids']
                                                    if item not in deleted_ids]

    # get the list of keyrefs to update
    updated_keyrefs = []
    for keyref, values in request.session['keyrefs'].iteritems():
        updated_keyrefs.extend(values['module_ids'])

    return HttpResponse(json.dumps(updated_keyrefs), content_type='application/javascript')
