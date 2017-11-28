""" Pop up module
"""
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class PopupModule(AbstractModule):
    """Popup module
    """
    def __init__(self, scripts=list(), styles=list(), popup_content=None, button_label='Save'):
        """Initializes the module

        :param scripts:
        :param styles:
        :param popup_content:
        :param button_label:
        """
        scripts = ['core_parser_app/js/builtin/popup.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)
        if popup_content is None:
            raise ModuleError("'popup_content' is required. Cannot instantiate an empty popup")

        self.popup_content = popup_content
        self.button_label = button_label

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        params = {
            "popup_content": self.popup_content,
            "button_label": self.button_label
        }

        return AbstractModule.render_module('core_parser_app/builtin/popup.html', params)
