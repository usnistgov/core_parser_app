""" Settings for core_parser_app

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from os.path import join, dirname, realpath

from django.conf import settings

if not settings.configured:
    settings.configure()

MODULES_ROOT = join(dirname(realpath(__file__)).replace("\\", "/"), "tools", "modules")

MODULE_TAG_NAME = getattr(settings, "MODULE_TAG_NAME", "module")

AUTO_ESCAPE_XML_ENTITIES = getattr(settings, "AUTO_ESCAPE_XML_ENTITIES", True)

PARSER_MAX_IN_MEMORY_ELEMENTS = getattr(
    settings, "PARSER_MAX_IN_MEMORY_ELEMENTS", 10000
)
""" Maximum number of in-memory elements allowed by the system during the parsing of XML/XSD files.
A large number of elements may cause performance issues.
"""
