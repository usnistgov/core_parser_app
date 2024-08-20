"""Auto discovery of modules
"""

import logging

from django.db import IntegrityError
from django.urls import URLPattern, URLResolver

from core_main_app.commons.exceptions import ModelError
from core_parser_app.components.module import api as module_api
from core_parser_app.components.module.models import Module
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule

logger = logging.getLogger(__name__)


def reload_modules(urls):
    """Reload modules in database

    :return:
    """
    logger.info("START discover modules.")

    try:
        # Remove all existing modules
        module_api.delete_all()
    except Exception as exc:
        logger.warning(str(exc))
        return

    # Look for modules in project urls
    try:
        for url in urls:
            if isinstance(url, URLPattern):
                _save_module(url)
            elif isinstance(url, URLResolver):
                for url_pattern in url.url_patterns:
                    _save_module(url_pattern)
    except ModelError:
        # something went wrong, delete already added modules
        error_msg = (
            "A validation error occurred during the module discovery. "
            "Please provide a name to all modules urls using the name argument."
        )

        logger.error(
            "Discover modules failed with error %s. All modules will be deleted.",
            error_msg,
        )
        module_api.delete_all()
        raise ModuleError(error_msg)
    except Exception as exception:
        # something went wrong, delete already added modules
        logger.error(
            "Discover modules failed with error %s. All modules will be deleted.",
            str(exception),
        )
        module_api.delete_all()
        raise exception

    logger.info("FINISH discover modules.")


def _save_module(url_pattern):
    """Save module from a URL pattern

    Args:
        url_pattern:

    Returns:

    """
    module_view_name = _get_module_view_name_from_url(url_pattern)
    if module_view_name.startswith("core_module_"):
        module_view = AbstractModule.get_view_from_view_path(module_view_name)
        if issubclass(module_view, AbstractModule):
            module_object = Module(
                url=url_pattern.pattern.regex.pattern,
                name=url_pattern.name,
                view=module_view_name,
                multiple=module_view.is_managing_occurrences,
            )
            try:
                module_api.upsert(module_object)
            except IntegrityError:
                logger.info(
                    "The module %s is already present in the database.",
                    url_pattern.name,
                )


def _get_module_view_name_from_url(url_pattern):
    """

    Args:
        url_pattern:

    Returns:

    """
    return url_pattern.lookup_str if hasattr(url_pattern, "lookup_str") else ""
