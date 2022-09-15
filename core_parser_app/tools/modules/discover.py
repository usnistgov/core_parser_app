"""Auto discovery of modules
"""
import logging

from django.db import IntegrityError

from core_main_app.commons.exceptions import ModelError
from core_parser_app.components.module import api as module_api
from core_parser_app.components.module.models import Module
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule

logger = logging.getLogger(__name__)


def discover_modules(urls):
    """

    :return:
    """
    logger.info("START discover modules.")

    try:
        # Remove all existing modules
        module_api.delete_all()
    except Exception:
        logger.warning("Module table is not ready yet")
        return

    # Look for modules in project urls
    try:
        for url in urls:
            if hasattr(url, "url_patterns"):
                for url_pattern in url.url_patterns:
                    module_view_name = (
                        url_pattern.lookup_str
                        if hasattr(url_pattern, "lookup_str")
                        else ""
                    )
                    if module_view_name.startswith("core_module_"):
                        module_view = AbstractModule.get_view_from_view_path(
                            module_view_name
                        )
                        if issubclass(module_view, AbstractModule):
                            # FIXME: do not use private field
                            module_object = Module(
                                url=url_pattern.pattern._regex,
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
    except ModelError:
        # something went wrong, delete already added modules
        module_api.delete_all()

        error_msg = (
            "A validation error occurred during the module discovery. "
            "Please provide a name to all modules urls using the name argument."
        )

        logger.error("Discover modules failed with %s.", error_msg)

        raise ModuleError(error_msg)
    except Exception as exception:
        # something went wrong, delete already added modules
        module_api.delete_all()
        logger.error("Discover modules failed with %s.", str(exception))
        raise exception

    logger.info("FINISH discover modules.")
