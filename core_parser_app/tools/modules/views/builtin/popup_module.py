""" Pop up module
"""
from abc import ABCMeta, abstractmethod

from core_parser_app.tools.modules.views.module import AbstractModule


class AbstractPopupModule(AbstractModule, metaclass=ABCMeta):
    """Popup module"""

    def __init__(self, scripts=list(), styles=list(), button_label=""):
        """Initialize module

        Args:
            scripts:
            styles:
        """
        scripts = ["core_parser_app/js/builtin/popup.js"] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.button_label = button_label
        self.popup_content = ""

    def _render_module(self, request):
        """Return module's rendering

        Args:
            request:

        Returns:

        """
        module_id = None

        if self.request:
            module_id = self.request.GET.get("module_id", None)

        params = {
            "popup_content": self._get_popup_content(),
            "module_id": module_id,
            "button_label": self.button_label,
        }

        return AbstractModule.render_template(
            "core_parser_app/builtin/popup.html", params
        )

    @abstractmethod
    def _get_popup_content(self):
        """Process data to build the module"""
        raise NotImplementedError("not implemented")
