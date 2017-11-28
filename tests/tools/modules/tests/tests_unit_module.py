"""Module system unit testing
"""
import json
from unittest.case import TestCase

from bson.objectid import ObjectId
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from mock.mock import Mock, patch

from core_parser_app.components.data_structure_element.models import DataStructureElement
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class TestGetResources(TestCase):

    def test_get_resources_returns_http_response(self):
        scripts = ['script1.js', 'script2.js']
        styles = ['style1.css', 'style2.css']

        module_object = ModuleImplementation(scripts=scripts, styles=styles)

        response = module_object._get_resources()

        self.assertTrue(isinstance(response, HttpResponse))

    def test_get_resources_returns_scripts(self):
        scripts = ['script1.js', 'script2.js']
        styles = ['style1.css', 'style2.css']

        module_object = ModuleImplementation(scripts=scripts, styles=styles)

        response = module_object._get_resources()
        response_scripts = json.loads(response.content)['scripts']

        self.assertEquals(response_scripts, scripts)

    def test_get_resources_returns_styles(self):
        scripts = ['script1.js', 'script2.js']
        styles = ['style1.css', 'style2.css']

        module_object = ModuleImplementation(scripts=scripts, styles=styles)

        response = module_object._get_resources()
        response_styles = json.loads(response.content)['styles']

        self.assertEquals(response_styles, styles)


class TestGet(TestCase):
    @patch('core_parser_app.tools.modules.views.module.AbstractModule.render_module')
    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_get_returns_http_response(self, data_structure_element_get_by_id, render_module):
        request = HttpRequest()
        request.GET = {
            'module_id': str(ObjectId()),
            'url': '/url',
        }
        module_object = ModuleImplementation()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()
        render_module.return_value = ""

        response = module_object.get(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch('core_parser_app.tools.modules.views.module.AbstractModule.render_module')
    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_get_data_structure_element_contains_module_values(self, data_structure_element_get_by_id, render_module):
        request = HttpRequest()
        request.GET = {
            'module_id': str(ObjectId()),
            'url': '/url',
        }
        module_object = ModuleImplementation()

        data_structure_element = _create_mock_data_structure_element()
        data_structure_element_get_by_id.return_value = data_structure_element
        render_module.return_value = ""

        module_object.get(request)

        self.assertTrue(data_structure_element.options['data'] == "get module result")

    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_get_http_response_raises_error_when_module_returns_None(self, data_structure_element_get_by_id):
        request = HttpRequest()
        request.GET = {
            'module_id': str(ObjectId()),
            'url': '/url',
        }
        module_object = ModuleImplementationNone()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()

        with self.assertRaises(ModuleError):
            module_object._get(request)


class TestPost(TestCase):

    def test_post_no_module_id_returns_http_response_bad_request(self):
        request = HttpRequest()
        request.POST = {}

        module_object = ModuleImplementation()
        response = module_object.post(request)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))

    @patch('core_parser_app.tools.modules.views.module.AbstractModule.render_module')
    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_post_returns_http_response(self, data_structure_element_get_by_id, render_module):
        request = HttpRequest()
        request.POST = {
            'module_id': str(ObjectId()),
        }

        module_object = ModuleImplementation()

        data_structure_element_get_by_id.return_value = _create_mock_data_structure_element()
        render_module.return_value = ""

        response = module_object.post(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch('core_parser_app.tools.modules.views.module.AbstractModule.render_module')
    @patch('core_parser_app.components.data_structure_element.models.DataStructureElement.get_by_id')
    def test_post_data_structure_element_contains_module_values(self, data_structure_element_get_by_id, render_module):
        request = HttpRequest()
        request.POST = {
            'module_id': str(ObjectId()),
        }

        module_object = ModuleImplementation()

        data_structure_element = _create_mock_data_structure_element()
        data_structure_element_get_by_id.return_value = data_structure_element
        render_module.return_value = ""

        response = module_object.post(request)
        response_html = json.loads(response.content)['html']

        self.assertTrue(data_structure_element.options['data'] == "post module result")


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
