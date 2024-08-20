"""Load modules command
"""

from django.core.management.base import BaseCommand
from django.urls import get_resolver

from core_parser_app.tools.modules.discover import reload_modules


class Command(BaseCommand):
    help = "Reload modules from list of urls"

    def handle(self, *args, **options):
        """handle

        Args:
            *args:
            **options:

        Returns:

        """
        reload_modules(get_resolver().url_patterns)
        self.stdout.write(
            self.style.SUCCESS("Modules were reloaded in database.")
        )
