""" Core Parser App - Unit test views
"""
from unittest.mock import patch

from django.test import SimpleTestCase

from core_main_app.commons.exceptions import XSDError
from core_main_app.components.template.models import Template
from core_parser_app.views.common.views import get_context


class TestModuleManagerUserView(SimpleTestCase):
    """TestModuleManagerUserView"""

    @patch("core_main_app.components.template.api.get_by_id")
    def test_get_context_raises_xsd_error_when_template_has_wrong_format(
        self, mock_template_get_by_id
    ):
        """test_get_context_raises_xsd_error_when_template_has_wrong_format

        Returns:

        """
        # Arrange
        mock_template = _get_json_template()
        mock_template_get_by_id.return_value = mock_template

        # Act + Assert
        with self.assertRaises(XSDError):
            get_context(
                template_id=mock_template.id,
                url_previous_button=None,
                read_only=False,
                title="test",
                request=None,
            )


def _get_json_template():
    """Get JSON template

    Returns:

    """
    template = Template()
    template.format = Template.JSON
    template.id_field = 1
    template.content = "{}"
    return template
