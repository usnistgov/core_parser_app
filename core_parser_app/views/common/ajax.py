"""AJAX views
"""
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.utils.html import escape

from core_main_app.components.template import api as template_api
from core_parser_app.components.module import api as module_api


@login_required
def delete_module(request):
    """Deletes a module from a template
    Params:
        request:
    Return:
    """
    try:
        # get the parameters
        template_id = request.POST.get("templateID", None)
        xpath = request.POST.get("xpath", None)

        # get the template
        template = template_api.get_by_id(template_id, request=request)

        # delete the module
        module_api.delete_module(template, xpath, request=request)
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@login_required
def insert_module(request):
    """
    Insert a module in a template
    :param request:
    :return:
    """
    try:
        # get the parameters
        module_id = request.POST.get("moduleID", None)
        template_id = request.POST.get("templateID", None)
        xpath = request.POST.get("xpath", None)

        # get the template
        template = template_api.get_by_id(template_id, request=request)
        # add the module
        module_api.add_module(template, module_id, xpath, request=request)
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")
