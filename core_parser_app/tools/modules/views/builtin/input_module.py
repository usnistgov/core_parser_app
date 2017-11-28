""" Input Module
"""
from core_parser_app.tools.modules.views.module import AbstractModule


class InputModule(AbstractModule):
    """Input module
    """

    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None, disabled=False):
        """Initializes module

        :param scripts:
        :param styles:
        :param label:
        :param default_value:
        :param disabled:
        """
        scripts = ['core_parser_app/js/builtin/input.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.default_value = default_value
        self.disabled = disabled

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        if self.default_value is not None:
            params.update({"default_value": self.default_value})

        if self.disabled is not None:
            params.update({"disabled": self.disabled})

        return AbstractModule.render_module('core_parser_app/builtin/input.html', params)
