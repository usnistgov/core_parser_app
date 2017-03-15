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
        data = {
            'id': element.pk,
            'selected': True if element.value == 'true' else False,
        }
        return self._load_template('checkbox', data)

    def render_restriction(self, element):
        """

        :param element:
        :return:
        """
        data = {
            'id': element.pk,
            'selected': True if element.value == 'true' else False,
        }
        return self._load_template('checkbox', data)
