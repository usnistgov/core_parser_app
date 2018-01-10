""" Pop up module
"""
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class PopupModule(AbstractModule):
    """Popup module
    """
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

    def _retrieve_data(self, request):
        """ Retrieve module's data

        Args:
            request:

        Returns:

        """
        raise NotImplementedError("_retrieve_data method is not implemented.")

    def _render_data(self, request):
        """ Retrieve module's data rendering

        Args:
            request:

        Returns:

        """
        raise NotImplementedError("_render_data method is not implemented.")
