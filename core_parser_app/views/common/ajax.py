"""AJAX views
"""
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.utils.html import escape

from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.rest.template_version_manager.utils import (
    can_user_modify_template_version_manager,
)
from core_parser_app.components.module import api as module_api


@login_required
def delete_module(request):
    """
    Deletes a module from a template
    :param request:
    :return:
    """
    try:
        # get the parameters
        template_id = request.POST.get("templateID", None)
        xpath = request.POST.get("xpath", None)

        # get the template
        template = template_api.get(template_id)
        # TODO: move to api level
        template_version_manager = template_version_manager_api.get_by_version_id(
            template_id
        )
        can_user_modify_template_version_manager(template_version_manager, request.user)

        # delete the module
        module_api.delete_module(template, xpath)
    except Exception as e:
        return HttpResponseBadRequest(
            escape(str(e)), content_type="application/javascript"
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
        template = template_api.get(template_id)
        # TODO: move to api
        template_version_manager = template_version_manager_api.get_by_version_id(
            template_id
        )
        can_user_modify_template_version_manager(template_version_manager, request.user)

        # add the module
        module_api.add_module(template, module_id, xpath)
    except Exception as e:
        return HttpResponseBadRequest(
            escape(str(e)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")
