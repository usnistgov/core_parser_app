"""Parser test models
"""

from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from tests import rights


class Parser(models.Model):
    """Parser object"""

    class Meta:
        """Meta"""

        verbose_name = "tests"
        default_permissions = ()
        permissions = (
            (
                rights.MOCK_DATA_STRUCTURE_ACCESS,
                get_formatted_name(rights.MOCK_DATA_STRUCTURE_ACCESS),
            ),
            (
                rights.MOCK_ANON_DATA_STRUCTURE_ACCESS,
                get_formatted_name(rights.MOCK_ANON_DATA_STRUCTURE_ACCESS),
            ),
        )
