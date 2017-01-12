"""Core parser app admin views
"""

from django.http.response import HttpResponseBadRequest

from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.rendering import admin_render

from core_parser_app.settings import MODULE_TAG_NAME, MODULES_ROOT
from core_main_app.utils.xml import xsl_transform
from core_main_app.components.template import api as template_api
from core_parser_app.components.module import api as module_api
from os.path import join


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
                "is_raw": False
            },
            {
                "path": 'core_parser_app/admin/js/module_manager.js',
                "is_raw": False
            },
        ],
        "css": ['core_main_app/common/css/XMLTree.css']
    }

    try:
        # get the template
        template = template_api.get(template_id)
        # Get path to XSLT file
        xslt_path = join(MODULES_ROOT, 'resources', 'xsl', 'xsd2html4modules.xsl')

        xsd_tree_html = xsl_transform(template.content, _read_and_update_xslt_with_settings(xslt_path))

        # Get list of modules
        modules = module_api.get_all()

        # Get version manager
        version_manager = version_manager_api.get_from_version(template)
        context = {
            'xsdTree': xsd_tree_html,
            'modules': modules,
            'object': template,
            'version_manager': version_manager,
        }

        return admin_render(request,
                            'core_parser_app/admin/module_manager.html',
                            assets=assets,
                            context=context)
    except Exception, e:
        return HttpResponseBadRequest(e.message)


def _read_and_update_xslt_with_settings(xslt_file_path):
    """Reads the content of a file, and update it with the settings

    Args:
        xslt_file_path:

    Returns:

    """
    with open(xslt_file_path) as xslt_file:
        xslt_file_content = xslt_file.read()
        xslt_file_content = xslt_file_content.replace("module_tag_name", MODULE_TAG_NAME)
        return xslt_file_content
