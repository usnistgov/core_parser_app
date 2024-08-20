"""Module discover unit testing
"""

from unittest.case import TestCase
from unittest.mock import patch

from django.db import IntegrityError
from django.urls import re_path

from core_main_app.commons.exceptions import ModelError
from core_parser_app.tools.modules.discover import reload_modules
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class TestDiscoverModules(TestCase):
    """Test Discover Modules"""

    @patch("core_parser_app.components.module.api.delete_all")
    def test_discover_modules_stops_if_an_error_occurs_when_deleting_modules(
        self, mock_delete_all
    ):
        """test_discover_modules_stops_if_an_error_occurs_when_deleting_modules

        Returns:

        """
        mock_delete_all.side_effect = Exception()
        reload_modules([])
        self.assertTrue(mock_delete_all.called)

    @patch(
        "core_parser_app.tools.modules.views.module.AbstractModule.get_view_from_view_path"
    )
    @patch(
        "core_parser_app.tools.modules.discover._get_module_view_name_from_url"
    )
    @patch("core_parser_app.components.module.api.delete_all")
    @patch("core_parser_app.components.module.api.upsert")
    def test_discover_modules_deletes_modules_if_model_errors(
        self,
        mock_upsert,
        mock_delete_all,
        mock_get_module_view_name_from_url,
        mock_get_view_from_view_path,
    ):
        """test_discover_modules_deletes_modules_if_model_errors

        Returns:

        """
        mock_upsert.side_effect = ModelError("error")
        mock_get_module_view_name_from_url.return_value = "core_module_test"
        mock_get_view_from_view_path.return_value = ModuleTest
        with self.assertRaises(ModuleError):
            reload_modules(
                [re_path("module-test", ModuleTest, name="core_module_test")]
            )
        self.assertEqual(mock_delete_all.call_count, 2)

    @patch(
        "core_parser_app.tools.modules.views.module.AbstractModule.get_view_from_view_path"
    )
    @patch(
        "core_parser_app.tools.modules.discover._get_module_view_name_from_url"
    )
    @patch("core_parser_app.components.module.api.delete_all")
    @patch("core_parser_app.components.module.api.upsert")
    def test_discover_modules_deletes_modules_if_exception(
        self,
        mock_upsert,
        mock_delete_all,
        mock_get_module_view_name_from_url,
        mock_get_view_from_view_path,
    ):
        """test_discover_modules_deletes_modules_if_exception

        Returns:

        """
        mock_upsert.side_effect = Exception("error")
        mock_get_module_view_name_from_url.return_value = "core_module_test"
        mock_get_view_from_view_path.return_value = ModuleTest
        with self.assertRaises(Exception):
            reload_modules(
                [re_path("module-test", ModuleTest, name="core_module_test")]
            )
        self.assertEqual(mock_delete_all.call_count, 2)

    @patch(
        "core_parser_app.tools.modules.views.module.AbstractModule.get_view_from_view_path"
    )
    @patch(
        "core_parser_app.tools.modules.discover._get_module_view_name_from_url"
    )
    @patch("core_parser_app.components.module.api.delete_all")
    @patch("core_parser_app.components.module.api.upsert")
    def test_discover_continues_if_integrity_error(
        self,
        mock_upsert,
        mock_delete_all,
        mock_get_module_view_name_from_url,
        mock_get_view_from_view_path,
    ):
        """test_discover_modules_deletes_modules_if_integrity_error

        Returns:

        """
        mock_upsert.side_effect = IntegrityError("error")
        mock_get_module_view_name_from_url.return_value = "core_module_test"
        mock_get_view_from_view_path.return_value = ModuleTest
        reload_modules(
            [re_path("module-test", ModuleTest, name="core_module_test")]
        )
        self.assertEqual(mock_delete_all.call_count, 1)


class ModuleTest(AbstractModule):
    """ModuleTest"""

    def _render_module(self, request):
        pass

    def _retrieve_data(self, request):
        pass

    def _render_data(self, request):
        pass
