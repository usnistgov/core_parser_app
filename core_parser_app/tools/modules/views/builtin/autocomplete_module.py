"""Auto Complete Module
"""
from core_parser_app.tools.modules.views.module import AbstractModule


class AutoCompleteModule(AbstractModule):
    """ AutoCompleteModule class
    """

    def __init__(self, scripts=list(), styles=list(), label=None):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        """
        scripts = ['core_parser_app/js/builtin/autocomplete.js'] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        params = {}

        if 'data' in request.GET:
            params['value'] = request.GET['data']

        if self.label is not None:
            params.update({"label": self.label})

        return AbstractModule.render_module('core_parser_app/builtin/autocomplete.html', params)

    # Unimplemented method (to be implemented by children classes)
    def _get_module(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._get_module(self, request)

    def _get_display(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._get_display(self, request)

    def _get_result(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._get_result(self, request)

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._post_display(self, request)

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._post_result(self, request)
