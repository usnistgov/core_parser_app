""" Input Button Module
"""
from core_parser_app.tools.modules.views.module import AbstractModule


class InputButtonModule(AbstractModule):
    """Input Button module
    """
    def __init__(self, scripts=list(), styles=list(), button_label='Send', label=None, default_value=None):
        """Initializes the module

        :param scripts:
        :param styles:
        :param button_label:
        :param label:
        :param default_value:
        """
        AbstractModule.__init__(self, scripts=scripts, styles=styles)
        self.button_label = button_label
        self.label = label
        self.default_value = default_value

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        params = {"button_label": self.button_label}
        if self.label is not None:
            params.update({"label": self.label})
        if self.default_value is not None:
            params.update({"default_value": self.default_value})
        return AbstractModule.render_module('core_parser_app/builtin/input_button.html', params)
