""" Unit tests for DefaultRenderer class.
"""
from unittest import TestCase
from unittest.mock import MagicMock

from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.tools.parser.renderer import DefaultRenderer


class TestDefaultRendererInit(TestCase):
    """Unit tests for DefaultRenderer.__init__ method."""

    def test_template_list_not_dict_raises_type_error(self):
        """test_template_list_not_dict_raises_type_error"""
        with self.assertRaises(TypeError):
            DefaultRenderer(
                MagicMock(spec=DataStructureElement), "mock_template_dict_str"
            )

    def test_successful_execution_returns_default_renderer_object(self):
        """test_successful_execution_returns_default_renderer_object"""
        self.assertIsInstance(
            DefaultRenderer(MagicMock(spec=DataStructureElement), {}),
            DefaultRenderer,
        )


class TestDefaultRendererLoadTemplate(TestCase):
    """Unit tests for DefaultRenderer._load_template method."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_template_key = "mock_template_key"
        self.default_renderer = DefaultRenderer(
            MagicMock(spec=DataStructureElement)
        )

    def test_template_data_not_dict_raises_type_error(self):
        """test_template_data_not_dict_raises_type_error"""
        with self.assertRaises(TypeError):
            self.default_renderer._load_template(
                self.mock_template_key, "mock_data_str"
            )

    def test_successful_execution_returns_template_render(self):
        """test_successful_execution_returns_template_render"""
        self.default_renderer.templates[self.mock_template_key] = MagicMock()

        self.assertEqual(
            self.default_renderer._load_template(self.mock_template_key, {}),
            self.default_renderer.templates[self.mock_template_key].render({}),
        )
