""" Pop up module
"""
from abc import ABCMeta

from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class AbstractPopupModule(AbstractModule):
    """Popup module
    """
    __metaclass__ = ABCMeta

    def __init__(self, scripts=list(), styles=list(), popup_content=None, button_label='Save'):
        """ Initialize module

        Args:
            scripts:
            styles:
            popup_content:
            button_label:
        """
        scripts = ['core_parser_app/js/builtin/popup.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)
        if popup_content is None:
            raise ModuleError("'popup_content' is required. Cannot instantiate an empty popup")

        self.popup_content = popup_content
        self.button_label = button_label

    def _render_module(self, request):
        """ Return module's rendering

        Args:
            request:

        Returns:

        """
        params = {
            "popup_content": self.popup_content,
            "button_label": self.button_label
        }

        return AbstractModule.render_template('core_parser_app/builtin/popup.html', params)
