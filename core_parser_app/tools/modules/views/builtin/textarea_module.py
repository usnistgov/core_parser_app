""" Text area Module
"""

from core_parser_app.tools.modules.views.module import AbstractModule


class TextAreaModule(AbstractModule):
    """Text Area module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, data=''):
        """ Initialize module

        Args:

            scripts:
            styles:
            label:
            data:
        """
        scripts = ['core_parser_app/js/builtin/textarea.js'] + scripts
        styles = ['core_parser_app/css/builtin/textarea.css'] + styles
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.data = data

    def _render_module(self, request):
        """ Return module's rendering

        Args:
            request:

        Returns:

        """
        params = {"label": self.label,
                  'data': self.data}

        return AbstractModule.render_template('core_parser_app/builtin/textarea.html', params)

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
