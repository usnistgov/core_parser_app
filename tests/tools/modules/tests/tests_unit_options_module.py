"""Checkboxes module unit testing"""

from unittest.case import TestCase

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_parser_app.tools.modules.views.builtin.options_module import (
    AbstractOptionsModule,
)


class TestOptionsModule(TestCase):
    """Test options module"""

    def test_init_module_set_default_resources(self):
        """test_init_module_set_default_resources"""

        test_options = {"1": "Option One", "2": "Option Two"}
        module_object = OptionsModule(options=test_options, selected="1")

        self.assertEqual(
            module_object.scripts, ["core_parser_app/js/builtin/options.js"]
        )

    def test_render_module_with_options(self):
        """test_render_module_with_options"""

        test_options = {"1": "Option One", "2": "Option Two"}
        module_object = OptionsModule(options=test_options, selected="1")

        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)

        html_result = module_object._render_module(mock_request)
        self.assertTrue("Option One" in html_result)
        self.assertTrue("Option Two" in html_result)


class OptionsModule(AbstractOptionsModule):
    """Module Implementation"""

    def _retrieve_data(self, request):
        """_retrieve_data
        Args:
            request:

        Returns:
        """

        return "module result"

    def _render_data(self, request):
        """_render_data
        Args:
            request:

        Returns:
        """

        return "module display"
