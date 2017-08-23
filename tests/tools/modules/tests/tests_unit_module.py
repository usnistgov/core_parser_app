"""Module system unit testing
"""
from unittest.case import TestCase
from mock.mock import Mock, patch
from bson.objectid import ObjectId
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest

from core_parser_app.components.data_structure_element.models import DataStructureElement
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.module import AbstractModule
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


class TestGetResources(TestCase):

    def test_get_resources_returns_http_response(self):
        scripts = ['script1.js', 'script2.js']
        styles = ['style1.css', 'style2.css']

        module = ModuleImplementation(scripts=scripts, styles=styles)

        response = module._get_resources()

        self.assertTrue(isinstance(response, HttpResponse))

    def test_get_resources_returns_scripts(self):
        scripts = ['script1.js', 'script2.js']
        styles = ['style1.css', 'style2.css']

        module = ModuleImplementation(scripts=scripts, styles=styles)

        response = module._get_resources()
        response_scripts = json.loads(response.content)['scripts']

        self.assertEquals(response_scripts, scripts)

    def test_get_resources_returns_styles(self):
        scripts = ['script1.js', 'script2.js']
        styles = ['style1.css', 'style2.css']

        module = ModuleImplementation(scripts=scripts, styles=styles)

        response = module._get_resources()
        response_styles = json.loads(response.content)['styles']

        self.assertEquals(response_styles, styles)


class TestRenderModule(TestCase):

    def test_render_module_returns_html_string(self):
        template_path = os.path.join(DATA_PATH, 'template.html')

        html_string = AbstractModule.render_module(template_path)

        with open(template_path, 'r') as template_file:
            expected_string = template_file.read()

        self.assertEquals(html_string, expected_string)


class TestGet(TestCase):
    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_get_returns_http_response(self, data_structure_element_get_by_id):
        request = HttpRequest()
        request.GET = {
            'module_id': str(ObjectId()),
            'url': '/url',
        }
        module = ModuleImplementation()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()

        response = module._get(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_get_http_response_contains_module_values(self, data_structure_element_get_by_id):
        request = HttpRequest()
        request.GET = {
            'module_id': str(ObjectId()),
            'url': '/url',
        }
        module = ModuleImplementation()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()

        response = module._get(request)

        self.assertTrue(module._get_module(request) in response.content)
        self.assertTrue(module._get_display(request) in response.content)

    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_get_http_response_raises_error_when_module_returns_None(self, data_structure_element_get_by_id):
        request = HttpRequest()
        request.GET = {
            'module_id': str(ObjectId()),
            'url': '/url',
        }
        module = ModuleImplementationNone()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()

        with self.assertRaises(ModuleError):
            module._get(request)


class TestPost(TestCase):

    def test_post_no_module_id_returns_http_response_bad_request(self):
        request = HttpRequest()
        request.POST = {}

        module = ModuleImplementation()
        response = module._post(request)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))

    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_post_returns_http_response(self, data_structure_element_get_by_id):
        request = HttpRequest()
        request.POST = {
            'module_id': str(ObjectId()),
        }

        module = ModuleImplementation()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()

        response = module._post(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_post_response_contains_module_values(self, data_structure_element_get_by_id):
        request = HttpRequest()
        request.POST = {
            'module_id': str(ObjectId()),
        }

        module = ModuleImplementation()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()

        response = module._post(request)
        response_html = json.loads(response.content)['html']

        self.assertTrue(module._post_display(request) in response_html)


def _create_mock_data_structure_element():
    """
    Returns a mock data structure element
    :return:
    """
    mock_element = Mock(spec=DataStructureElement)
    mock_element.tag = "tag"
    mock_element.value = "value"
    mock_element.options = {}
    mock_element.children = []
    return mock_element


class ModuleImplementation(AbstractModule):

    def _get_module(self, request):
        return "get module content"

    def _get_display(self, request):
        return "get module display"

    def _get_result(self, request):
        return "get module result"

    def _post_display(self, request):
        return "post module display"

    def _post_result(self, request):
        return "post module result"


class ModuleImplementationNone(AbstractModule):

    def _get_module(self, request):
        return None

    def _get_display(self, request):
        return None

    def _get_result(self, request):
        return None

    def _post_display(self, request):
        return None

    def _post_result(self, request):
        return None
