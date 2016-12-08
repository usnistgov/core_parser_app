"""Checkbox Renderer class
"""
import logging

from core_parser_app.tools.parser.renderer.list import ListRenderer

logger = logging.getLogger(__name__)


class CheckboxRenderer(ListRenderer):
    """
    """

    def _render_input(self, element):
        """

        :param element
        :return:
        """
        return self._load_template('checkbox')

    def render_restriction(self, element):
        """

        :param element:
        :return:
        """
        return self._load_template('checkbox')
