""" Text area Module
"""

from core_parser_app.tools.modules.views.module import AbstractModule


class TextAreaModule(AbstractModule):
    """Text Area module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, data=''):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        :param data:
        """
        scripts = ['core_parser_app/js/builtin/textarea.js'] + scripts
        styles = ['core_parser_app/css/builtin/textarea.css'] + styles
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.data = data

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        params = {"label": self.label,
                  'data': self.data}

        return AbstractModule.render_module('core_parser_app/builtin/textarea.html', params)
