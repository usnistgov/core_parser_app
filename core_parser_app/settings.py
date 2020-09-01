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
