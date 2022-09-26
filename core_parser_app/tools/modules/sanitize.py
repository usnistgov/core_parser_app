"""Sanitize util
"""
import json
import logging
from builtins import str

from django.utils.html import escape
from lxml import etree

from xml_utils.commons.exceptions import XMLError
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


def sanitize(input_value):
    """Sanitize the strings in the input

    :param input_value:
    :return:
    """
    # get the type of the input
    input_type = type(input_value)

    # input is a list
    if input_type == list:
        clean_value = []
        for item in input_value:
            clean_value.append(sanitize(item))

        return clean_value
    # input is a dict
    elif input_type == dict:
        return {
            sanitize(key): sanitize(val)
            for key, val in list(input_value.items())
        }
    # input is a string of characters
    elif input_type == str:
        try:
            # XML cleaning
            xml_cleaner_parser = etree.XMLParser(remove_blank_text=True)
            xml_data = XSDTree.fromstring(
                input_value, parser=xml_cleaner_parser
            )

            input_value = XSDTree.tostring(xml_data)
        except XMLError as e:
            # input is not XML, pass
            logger.warning("sanitize threw an exception: {0}".format(str(e)))

        finally:
            try:
                json_value = json.loads(input_value)
                sanitized_value = sanitize(json_value)

                clean_value = json.dumps(sanitized_value)
            except ValueError:
                clean_value = escape(input_value)

        return clean_value
    # input is a number
    elif input_type == int or input_type == float:
        return input_value
    # default, escape characters
    else:
        # Default sanitizing
        return escape(str(input_value))
