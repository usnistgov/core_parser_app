"""Abstract Class Module
"""
import os
from django.http import HttpResponse
import json
import importlib

from django.http.response import HttpResponseBadRequest
from django.template import Context, Template
from django.utils import importlib
from rest_framework.status import HTTP_200_OK
from exceptions import ModuleError
from abc import ABCMeta, abstractmethod

from core_parser_app.components.data_structure_element import api as data_structure_element_api
from core_parser_app.components.module import api as module_api
from core_parser_app.settings import MODULES_ROOT


class AbstractModule(object):
    """Abstract module class
    """
    __metaclass__ = ABCMeta

    def __init__(self, scripts=list(), styles=list()):
        """Initializes the module

        :param scripts:
        :param styles:
        """
        # JS scripts
        self.scripts = scripts
        # CSS spreadsheets
        self.styles = styles

        # Is the module managing occurrences by its own? (False by default)
        self.is_managing_occurrences = False

        # Skeleton of the modules
        self.template = os.path.join(MODULES_ROOT, 'resources', 'html', 'module.html')

    def render(self, request):
        """Renders the module

        :param request:
        :return:
        """
        if request.method == 'GET':
            if 'resources' in request.GET:
                return self._get_resources()
            elif 'managing_occurrences' in request.GET:
                return HttpResponse(json.dumps(self.is_managing_occurrences), HTTP_200_OK)
            else:
                return self._get(request)
        elif request.method == 'POST':
            return self._post(request)
        else:
            raise ModuleError('Only GET and POST methods can be used to communicate with a module.')

    def _get(self, request):
        """Manages the GET requests

        :param request:
        :return:
        """
        module_id = request.GET['module_id']
        url = request.GET['url'] if 'url' in request.GET else \
            data_structure_element_api.get_by_id(module_id) .options['url']
        template_data = {
            'module_id': module_id,
            'module': '',
            'display': '',
            'url': url
        }

        try:
            # get values from module
            template_data['module'] = self._get_module(request)
            template_data['display'] = self._get_display(request)

            # get module element
            module_element = data_structure_element_api.get_by_id(module_id)
            # get its options
            options = module_element.options
            # update module element data
            options['data'] = self._get_result(request)
            # set updated options
            module_element.options = options
            # save module element
            data_structure_element_api.upsert(module_element)
        except Exception, e:
            raise ModuleError('Something went wrong during module initialization: ' + e.message)

        # Check that values are not None
        for key, val in template_data.items():
            if val is None:
                raise ModuleError('Variable '+key+' cannot be None. Module initialization cannot be completed.')

        # TODO Add additional checks

        # Apply tags to the template
        html_string = AbstractModule.render_module(self.template, template_data)
        return HttpResponse(html_string, status=HTTP_200_OK)

    def _post(self, request):
        """Manages the POST requests

        :param request:
        :return:
        """
        template_data = {
            'display': '',
            'url': ''
        }

        try:
            if 'module_id' not in request.POST:
                return HttpResponseBadRequest({'error': 'No "module_id" parameter provided'})

            module_element = data_structure_element_api.get_by_id(request.POST['module_id'])
            template_data['display'] = self._post_display(request)
            options = module_element.options

            # TODO temporary solution
            post_result = self._post_result(request)

            if type(post_result) == dict:
                options['data'] = self._post_result(request)['data']
                options['attributes'] = self._post_result(request)['attributes']
            else:
                options['data'] = post_result

            # TODO Implement this system instead
            # options['content'] = self._get_content(request)
            # options['attributes'] = self._get_attributes(request)

            module_element.options = options
            data_structure_element_api.upsert(module_element)
        except Exception, e:
            raise ModuleError('Something went wrong during module update: ' + e.message)

        html_code = AbstractModule.render_module(self.template, template_data)

        response_dict = dict()
        response_dict['html'] = html_code

        if hasattr(self, "get_XpathAccessor"):
            response_dict.update(self.get_XpathAccessor())

        return HttpResponse(json.dumps(response_dict))

    def _get_resources(self):
        """Returns HTTP response containing module resources
        """
        response = {
            'scripts': self.scripts,
            'styles': self.styles
        }

        return HttpResponse(json.dumps(response), status=HTTP_200_OK)

    @abstractmethod
    def _get_module(self, request):
        """Returns the module content

        :param request:
        :return:
        """
        raise NotImplementedError("_get_module method is not implemented.")

    @abstractmethod
    def _get_display(self, request):
        """Returns the results to display after a GET request

        :param request:
        :return:
        """
        raise NotImplementedError("_get_display method is not implemented.")

    @abstractmethod
    def _get_result(self, request):
        """Returns the results to store after a GET request

        :param request:
        :return:
        """
        raise NotImplementedError("_get_result method is not implemented.")

    @abstractmethod
    def _post_display(self, request):
        """Returns the results to display after a POST request

        :param request:
        :return:
        """
        raise NotImplementedError("_post_display method is not implemented.")

    @abstractmethod
    def _post_result(self, request):
        """Returns the results to store after a GET request

        :param request:
        :return:
        """
        raise NotImplementedError("_post_result method is not implemented.")

    @staticmethod
    def get_module_view(url):
        """Returns module view from an url

        :param url:
        :return:
        """
        module = module_api.get_by_url(url)
        return AbstractModule.get_view_from_view_path(module.view)

    @staticmethod
    def get_view_from_view_path(view):
        """Returns module view from its view string

        :param view:
        :return:
        """
        # module = module_api.get_by_url(url)
        pkglist = view.split('.')

        pkgs = '.'.join(pkglist[:-1])
        func = pkglist[-1:][0]

        imported_pkgs = importlib.import_module(pkgs)
        return getattr(imported_pkgs, func)

    @staticmethod
    def render_module(template, params=None):
        """Renders the module in HTML using django template

        :param template: path to HTML template to render
        :param params: parameters to create a context for the template
        :return:
        """
        if params is None:
            params = {}

        with open(template, 'r') as template_file:
            template_content = template_file.read()

            template = Template(template_content)
            context = Context(params)

            return template.render(context)
