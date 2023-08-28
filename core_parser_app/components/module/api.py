"""API for modules
"""
from core_main_app.commons.exceptions import XSDError
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from xml_utils.xsd_tree.operations.appinfo import (
    add_appinfo_element,
    delete_appinfo_element,
)
from core_parser_app.components.module.models import Module
from core_parser_app.settings import MODULE_TAG_NAME


def get_by_id(module_id):
    """Returns a module by its id

    Args:
        module_id:

    Returns:

    """
    return Module.get_by_id(module_id)


def get_by_url(module_url):
    """Returns a module by its url

    Args:
        module_url:

    Returns:

    """
    return Module.get_by_url(module_url)


def upsert(module):
    """Saves or updates a module

    Args:
        module:

    Returns:

    """
    return module.save()


def get_all():
    """Returns all modules

    Returns:

    """
    return Module.get_all()


def get_all_urls():
    """Returns all modules urls

    Returns:

    """
    return Module.get_all_urls()


def delete_all():
    """Deletes all modules

    Returns:

    """
    Module.delete_all()


def add_module(template, module_id, xpath, request):
    """Inserts a module in a template

    Args:
        template:
        module_id:
        xpath:
        request:

    Returns:

    """
    # check template format
    if template.format != Template.XSD:
        raise XSDError("The template is not an XML Schema")

    # get the module
    module_object = get_by_id(module_id)

    template.content = add_appinfo_element(
        template.content, xpath, MODULE_TAG_NAME, module_object.url
    )
    return template_api.upsert(template, request=request)


def delete_module(template, xpath, request):
    """Deletes a module from a template

    Args:
        template:
        xpath:
        request:

    Returns:

    """
    # check template format
    if template.format != Template.XSD:
        raise XSDError("The template is not an XML Schema")

    # delete module attribute from element
    template.content = delete_appinfo_element(
        template.content, xpath, MODULE_TAG_NAME
    )

    return template_api.upsert(template, request=request)
