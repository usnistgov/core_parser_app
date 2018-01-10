""" Input Module
"""
from core_parser_app.tools.modules.views.module import AbstractModule


class InputModule(AbstractModule):
    """Input module
    """

    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None, disabled=False):
        """ Initialize the module

        Args:
            scripts:
            styles:
            label:
            default_value:
            disabled:
        """
        scripts = ['core_parser_app/js/builtin/input.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.default_value = default_value
        self.disabled = disabled

    def _render_module(self, request):
        """ Return module's rendering

        Args:
            request:

        Returns:

        """
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        if self.default_value is not None:
            params.update({"default_value": self.default_value})

        if self.disabled is not None:
            params.update({"disabled": self.disabled})

        return AbstractModule.render_template('core_parser_app/builtin/input.html', params)

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
