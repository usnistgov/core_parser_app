""" Unit tests for AbstractListRenderer class.
"""
from unittest import TestCase
from unittest.mock import MagicMock

from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.tools.parser.renderer.list import AbstractListRenderer


class TestAbstractListRendererRenderUl(TestCase):
    """Unit tests for `AbstractListRenderer._render_ul` method."""

    def setUp(self) -> None:
        """setUp"""
        self.renderer = AbstractListRenderer(
            MagicMock(spec=DataStructureElement)
        )
        self.mock_kwargs = {
            "content": "mock_content",
            "element_id": "mock_element_id",
            "is_hidden": True,
        }

    def test_element_id_not_str_raises_type_error(self):
        """test_element_id_not_str_raises_type_error"""
        self.mock_kwargs["element_id"] = 42  # noqa

        with self.assertRaises(TypeError):
            self.renderer._render_ul(**self.mock_kwargs)

    def test_is_hidden_not_bool_raises_type_error(self):
        """test_is_hidden_not_bool_raises_type_error"""
        self.mock_kwargs["is_hidden"] = "mock_is_hidden"  # noqa

        with self.assertRaises(TypeError):
            self.renderer._render_ul(**self.mock_kwargs)

    def test_successful_execution_returns_load_template(self):
        """test_successful_execution_returns_load_template"""
        self.assertEqual(
            self.renderer._render_ul(**self.mock_kwargs),
            self.renderer._load_template("ul", self.mock_kwargs),
        )
