"""
    Common views
"""
from django.contrib.staticfiles import finders
from django.http.response import HttpResponseBadRequest
from django.urls import reverse

from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.rendering import render
from core_main_app.utils.xml import xsl_transform
from core_parser_app.components.module import api as module_api
from core_parser_app.settings import MODULE_TAG_NAME


def manage_template_modules(request, template_id):
    """View that allows module management

    Args:
        request:
        template_id:

    Returns:

    """

    assets = {
        "js": [
            {
                "path": 'core_main_app/common/js/XMLTree.js',
                "is_raw": True
            },
            {
                "path": 'core_parser_app/common/js/module_manager.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/common/js/backtoprevious.js',
                "is_raw": True
            }
        ],
        "css": ['core_main_app/common/css/XMLTree.css',
                'core_parser_app/common/css/modules.css']
    }

    modals = ["core_parser_app/common/modals/add_module.html"]

    try:
        return render(request,
                      'core_parser_app/common/module_manager.html',
                      modals=modals,
                      assets=assets,
                      context=get_context(template_id, "core_main_app_manage_template_versions"))
    except Exception, e:
        return HttpResponseBadRequest(e.message)


def get_context(template_id, url_previous_button):
    """ Get the context to manage the template modules

    Args: template_id:
    Returns:
    """

    # get the template
    template = template_api.get(template_id)
    # Get path to XSLT file
    xslt_path = finders.find('core_parser_app/xsl/xsd2html4modules.xsl')
    xsd_tree_html = xsl_transform(template.content, read_and_update_xslt_with_settings(xslt_path))
    # Get list of modules
    modules = module_api.get_all()
    # Get version manager
    version_manager = version_manager_api.get_from_version(template)
    context = {
        'xsdTree': xsd_tree_html,
        'modules': modules,
        'object': template,
        'version_manager': version_manager,
        'url_back_to': reverse(url_previous_button, kwargs={'version_manager_id': version_manager.id}),
    }
    return context


def read_and_update_xslt_with_settings(xslt_file_path):
    """Read the content of a file, and update it with the settings

    Args:
        xslt_file_path:

    Returns:

    """
    with open(xslt_file_path) as xslt_file:
        xslt_file_content = xslt_file.read()
        xslt_file_content = xslt_file_content.replace("module_tag_name", MODULE_TAG_NAME)
        return xslt_file_content
