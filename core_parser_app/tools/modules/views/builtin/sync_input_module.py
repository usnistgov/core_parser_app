""" Synchronous Input Module
"""
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class SyncInputModule(AbstractModule):
    """Synchronous input module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None, modclass=None, disabled=False):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        :param default_value:
        :param modclass:
        :param disabled:
        """
        scripts = ['core_parser_app/js/builtin/sync_input.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        if modclass is None:
            raise ModuleError("'modclass' is required.")

        self.modclass = modclass
        self.label = label
        self.default_value = default_value
        self.disabled = disabled

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """

        params = {'class': self.modclass}
        if self.label is not None:
            params.update({"label": self.label})
        if self.default_value is not None:
            params.update({"default_value": self.default_value})
        if self.disabled is not None:
            params.update({"disabled": self.disabled})
        return AbstractModule.render_module('core_parser_app/builtin/sync_input.html', params)
