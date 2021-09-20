"""XML utils
"""
import logging
from urllib.parse import urlparse

from core_parser_app.components.module import api as module_api
from core_parser_app.settings import MODULE_TAG_NAME
from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE

logger = logging.getLogger(__name__)

APP_INFO_OPTIONS = [
    "label",
    "placeholder",
    "tooltip",
    "use",
    "default",
    MODULE_TAG_NAME,
]


def get_app_info_options(element):
    """Gets app info options of the element if present. Options are specific to the parser

    Args:
        element:

    Returns:

    """
    # Initialize dictionary to return
    app_info = {}

    # Get app info of the element
    app_info_elements = element.findall(
        "./{0}annotation/{0}appinfo".format(LXML_SCHEMA_NAMESPACE)
    )
    # Browse the app info
    for app_info_element in app_info_elements:
        # get the elements in the app info
        for app_info_child in app_info_element.getchildren():
            # look for parser options in the app info elements
            for option in APP_INFO_OPTIONS:
                # if the option is found
                if option in app_info_child.tag:
                    # set the option with its value
                    app_info[option] = app_info_child.text

    # return the app info dictionary
    return app_info


def delete_annotations(element):
    """Delete annotations from element

    Args:
        element:

    Returns:

    """
    annotations = element.findall("./{0}annotation".format(LXML_SCHEMA_NAMESPACE))
    for annotation in annotations:
        element.remove(annotation)


def get_element_occurrences(element):
    """Gets min/max occurrences information of the element

    Args:
        element:

    Returns:

    """
    # default values if attribute is absent
    min_occurs = 1
    max_occurs = 1

    # Get min occurs
    if "minOccurs" in element.attrib:
        min_occurs = int(element.attrib["minOccurs"])

    # Get max occurs
    if "maxOccurs" in element.attrib:
        if element.attrib["maxOccurs"] == "unbounded":
            max_occurs = -1
        else:
            max_occurs = int(element.attrib["maxOccurs"])

    return min_occurs, max_occurs


def get_attribute_occurrences(element):
    """Gets min/max occurrences information of the attribute

    Args:
        element:

    Returns:

    """
    # FIXME attribute use defaults to optional not required
    min_occurs = 1
    max_occurs = 1

    if "use" in element.attrib:
        if element.attrib["use"] == "optional":
            min_occurs = 0
        elif element.attrib["use"] == "prohibited":
            min_occurs = 0
            max_occurs = 0
        elif element.attrib["use"] == "required":
            logger.debug("get_attribute_occurrences: element use required")

    return min_occurs, max_occurs


def get_module_url(element):
    """Gets url of the module attached to element

    Args:
        element:

    Returns:

    """
    # get the app info of the element
    app_info = get_app_info_options(element)

    # check if a module is set for this element
    if MODULE_TAG_NAME in app_info:
        # get the url of the module
        app_info_url = app_info[MODULE_TAG_NAME]

        # parse the url
        parsed_url = urlparse(app_info_url)

        # get the url path
        url_path = parsed_url.path

        # check that the url is registered in the system
        if url_path in module_api.get_all_urls():
            return parsed_url

    return None
