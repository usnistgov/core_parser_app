"""Core parser app config
"""

from django.apps import AppConfig
from core_parser_app.tools.modules import discover


class CoreParserAppConfig(AppConfig):
    name = 'core_parser_app'
    verbose_name = "Core Parser App"

    def ready(self):
        """Run once at startup

        :return:
        """
        discover.discover_modules()
