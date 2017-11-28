"""Auto discovery of modules
"""
from mongoengine.errors import ValidationError

from core_parser_app.components.module import api as module_api
from core_parser_app.components.module.models import Module
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


def discover_modules(urls):
    """

    :return:
    """
    # Remove all existing modules
    module_api.delete_all()

    # Look for modules in project urls
    try:
        for url in urls:
            for url_pattern in url.url_patterns:
                module_view_name = url_pattern.lookup_str if hasattr(url_pattern, 'lookup_str') else ''
                if module_view_name.startswith('core_module_'):
                    module_view = AbstractModule.get_view_from_view_path(module_view_name)
                    if issubclass(module_view, AbstractModule):
                        module_object = Module(url=url_pattern.regex.pattern,
                                               name=url_pattern.name,
                                               view=module_view_name,
                                               multiple=module_view.is_managing_occurrences)
                        module_api.upsert(module_object)
    except ValidationError:
        # something went wrong, delete already added modules
        module_api.delete_all()

        error_msg = 'A validation error occurred during the module discovery. ' \
                    'Please provide a name to all modules urls using the name argument.'
        raise ModuleError(error_msg)
    except Exception, e:
        # something went wrong, delete already added modules
        module_api.delete_all()
        raise e
