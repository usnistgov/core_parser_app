"""Auto Complete Module
"""
from core_parser_app.tools.modules.views.module import AbstractModule


class AutoCompleteModule(AbstractModule):
    """ AutoCompleteModule class
    """

    def __init__(self, scripts=list(), styles=list(), label=None):
        """ Initialize the module

        Args:
            scripts:
            styles:
            label:
        """
        scripts = ['core_parser_app/js/builtin/autocomplete.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label

    def _render_module(self, request):
        """ Return the module

        Args:
            request:

        Returns:

        """
        params = {}

        if self.data != '':
            params['value'] = self.data

        if self.label is not None:
            params.update({"label": self.label})

        return AbstractModule.render_template('core_parser_app/builtin/autocomplete.html', params)

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
