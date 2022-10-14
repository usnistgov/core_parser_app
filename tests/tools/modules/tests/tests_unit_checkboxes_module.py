"""Checkboxes module unit testing
"""
from unittest.case import TestCase

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_parser_app.tools.modules.views.builtin.checkboxes_module import (
    AbstractCheckboxesModule,
)


class TestInitCheckboxesModule(TestCase):
    """Test init checkboxes module"""

    def test_init_module_set_default_resources(self):
        """test_init_module_set_default_resources"""

        module_object = CheckboxModule(name="checkboxes")

        self.assertEqual(
            module_object.scripts, ["core_parser_app/js/builtin/checkboxes.js"]
        )
        self.assertEqual(
            module_object.styles,
            ["core_parser_app/css/builtin/checkboxes.css"],
        )

    def test_init_module_with_extra_script(self):
        """test_init_module_with_extra_script"""

        scripts = ["script1.js"]

        module_object = CheckboxModule(name="checkboxes", scripts=scripts)

        self.assertEqual(
            module_object.scripts,
            ["core_parser_app/js/builtin/checkboxes.js", "script1.js"],
        )

    def test_init_module_with_extra_style(self):
        """test_init_module_with_extra_style"""

        styles = ["style1.css"]

        module_object = CheckboxModule(name="checkboxes", styles=styles)

        self.assertEqual(
            module_object.styles,
            ["core_parser_app/css/builtin/checkboxes.css", "style1.css"],
        )


class TestRenderCheckboxesModule(TestCase):
    """Test division in checkboxes module"""

    def test_render_checkboxes_module_without_options(self):
        """test_render_checkboxes_module_without_options"""
        module_object = CheckboxModule(name="checkboxes")
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        html_result = module_object._render_module(mock_request)
        self.assertIsNotNone(html_result)

    def test_render_checkboxes_module_with_options(self):
        """test_render_checkboxes_module_with_options"""
        module_object = CheckboxModule(
            name="checkboxes", options={"1": "value1", "2": "value2"}
        )
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        html_result = module_object._render_module(mock_request)
        self.assertTrue("value1" in html_result)
        self.assertTrue("value2" in html_result)


class CheckboxModule(AbstractCheckboxesModule):
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
