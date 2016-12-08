from commons.constants import LXML_SCHEMA_NAMESPACE
from core_parser_app.settings import MODULE_TAG_NAME
from urlparse import urlparse
from core_parser_app.components.module import api as module_api

APP_INFO_OPTIONS = ['label', 'placeholder', 'tooltip', 'use', 'default', MODULE_TAG_NAME]


def get_app_info_options(element):
    """Get app info options of the element if present. Options are specific to the parser

    Args:
        element:

    Returns:

    """
    # Initialize dictionary to return
    app_info = {}

    # Get app info of the element
    app_info_elements = element.findall("./{0}annotation/{0}appinfo".format(LXML_SCHEMA_NAMESPACE))
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


def get_xsd_types(prefix):
    """Returns the list of all supported XSD types

    Args:
        prefix:

    Returns:

    """
    # FIXME Some datatypes are missing (https://www.w3.org/TR/xmlschema-2/#built-in-datatypes)
    if prefix != '':
        prefix += ':'
    return ["{0}anyType".format(prefix),
            "{0}string".format(prefix),
            "{0}normalizedString".format(prefix),
            "{0}token".format(prefix),
            "{0}duration".format(prefix),
            "{0}dateTime".format(prefix),
            "{0}time".format(prefix),
            "{0}date".format(prefix),
            "{0}gYearMonth".format(prefix),
            "{0}gYear".format(prefix),
            "{0}gMonthDay".format(prefix),
            "{0}gDay".format(prefix),
            "{0}gMonth".format(prefix),
            "{0}boolean".format(prefix),
            "{0}base64Binary".format(prefix),
            "{0}hexBinary".format(prefix),
            "{0}float".format(prefix),
            "{0}double".format(prefix),
            "{0}anyURI".format(prefix),
            "{0}QName".format(prefix),
            "{0}decimal".format(prefix),
            "{0}integer".format(prefix),
            "{0}nonPositiveInteger".format(prefix),
            "{0}negativeInteger".format(prefix),
            "{0}long".format(prefix),
            "{0}nonNegativeInteger".format(prefix),
            "{0}unsignedLong".format(prefix),
            "{0}positiveInteger".format(prefix),
            "{0}unsignedInt".format(prefix),
            "{0}unsignedShort".format(prefix),
            "{0}unsignedByte".format(prefix),
            "{0}long".format(prefix),
            "{0}int".format(prefix),
            "{0}short".format(prefix),
            "{0}byte".format(prefix)]


def get_target_namespace(namespaces, xsd_tree):
    """Returns the target namespace used in the schema

    Args:
        namespaces:
        xsd_tree:

    Returns:

    """
    root_attributes = xsd_tree.getroot().attrib
    target_namespace = root_attributes['targetNamespace'] if 'targetNamespace' in root_attributes else None
    target_namespace_prefix = ''
    if target_namespace is not None:
        for prefix, url in namespaces.items():
            if url == target_namespace:
                target_namespace_prefix = prefix
                break

    return target_namespace, target_namespace_prefix


def get_element_occurrences(element):
    """Get min/max occurrences information of the element

    Args:
        element:

    Returns:

    """
    # default values if attribute is absent
    min_occurs = 1
    max_occurs = 1

    # Get min occurs
    if 'minOccurs' in element.attrib:
        min_occurs = int(element.attrib['minOccurs'])

    # Get max occurs
    if 'maxOccurs' in element.attrib:
        if element.attrib['maxOccurs'] == "unbounded":
            max_occurs = -1
        else:
            max_occurs = int(element.attrib['maxOccurs'])

    return min_occurs, max_occurs


def get_attribute_occurrences(element):
    """Get min/max occurrences information of the attribute

    Args:
        element:

    Returns:

    """
    # FIXME attribute use defaults to optional not required
    min_occurs = 1
    max_occurs = 1

    if 'use' in element.attrib:
        if element.attrib['use'] == "optional":
            min_occurs = 0
        elif element.attrib['use'] == "prohibited":
            min_occurs = 0
            max_occurs = 0
        elif element.attrib['use'] == "required":
            pass

    return min_occurs, max_occurs


def get_module_url(element):
    """

    Args:
        element:

    Returns:

    """
    # FIXME: session removed, explore will display modules
    # if request.session['PARSER_IGNORE_MODULES']:
    #     return False

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
