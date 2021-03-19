"""Parser test models
"""

from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from tests import rights


class Parser(models.Model):
    class Meta(object):
        verbose_name = "tests"
        default_permissions = ()
        permissions = (
            (
                rights.mock_data_structure_access,
                get_formatted_name(rights.mock_data_structure_access),
            ),
            (
                rights.mock_anon_data_structure_access,
                get_formatted_name(rights.mock_anon_data_structure_access),
            ),
        )
