"""Module system unit testing
"""
import json
from unittest.case import TestCase

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from mock.mock import Mock, patch

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class TestGetResources(TestCase):
    def test_get_resources_returns_http_response(self):
        scripts = ["script1.js", "script2.js"]
        styles = ["style1.css", "style2.css"]

        module_object = ModuleImplementation(scripts=scripts, styles=styles)

        response = module_object._get_resources()

        self.assertTrue(isinstance(response, HttpResponse))

    def test_get_resources_returns_scripts(self):
        scripts = ["script1.js", "script2.js"]
        styles = ["style1.css", "style2.css"]

        module_object = ModuleImplementation(scripts=scripts, styles=styles)

        response = module_object._get_resources()
        response_scripts = json.loads(response.content)["scripts"]

        self.assertEquals(response_scripts, scripts)

    def test_get_resources_returns_styles(self):
        scripts = ["script1.js", "script2.js"]
        styles = ["style1.css", "style2.css"]

        module_object = ModuleImplementation(scripts=scripts, styles=styles)

        response = module_object._get_resources()
        response_styles = json.loads(response.content)["styles"]

        self.assertEquals(response_styles, styles)


class TestGet(TestCase):
    @patch("core_parser_app.tools.modules.views.module.AbstractModule.render_template")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    @patch("core_parser_app.components.data_structure_element.api.upsert")
    def test_get_returns_http_response(
        self,
        mock_data_structure_element_upsert,
        mock_data_structure_element_get_by_id,
        mock_render_template,
    ):
        request = HttpRequest()
        request.GET = {
            "module_id": "1",
            "url": "/url",
        }
        request.user = create_mock_user("1")
        module_object = ModuleImplementation()

        mock_data_structure_element = _create_mock_data_structure_element()
        mock_data_structure_element_get_by_id.return_value = mock_data_structure_element
        mock_data_structure_element_upsert.return_value = mock_data_structure_element
        mock_render_template.return_value = ""

        response = module_object.get(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch("core_parser_app.tools.modules.views.module.AbstractModule.render_template")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    @patch("core_parser_app.components.data_structure_element.api.upsert")
    def test_get_data_structure_element_contains_module_values(
        self,
        mock_data_structure_element_upsert,
        mock_data_structure_element_get_by_id,
        mock_render_template,
    ):
        request = HttpRequest()
        request.GET = {
            "module_id": "1",
            "url": "/url",
        }
        request.user = create_mock_user("1")
        module_object = ModuleImplementation()

        data_structure_element = _create_mock_data_structure_element()
        mock_data_structure_element_get_by_id.return_value = data_structure_element
        mock_data_structure_element_upsert.return_value = data_structure_element
        mock_render_template.return_value = ""

        module_object.get(request)

        self.assertTrue(data_structure_element.options["data"] == "module result")

    @patch(
        "core_parser_app.components.data_structure.models.DataStructureElement.get_by_id"
    )
    def test_get_http_response_raises_error_when_module_returns_None(
        self, data_structure_element_get_by_id
    ):
        request = HttpRequest()
        request.GET = {
            "module_id": "1",
            "url": "/url",
        }
        module_object = ModuleImplementationNone()

        data_structure_element_get_by_id.return_value = (
            _create_mock_data_structure_element()
        )

        with self.assertRaises(ModuleError):
            module_object._get(request)


class TestPost(TestCase):
    def test_post_no_module_id_returns_http_response_bad_request(self):
        request = HttpRequest()
        request.POST = {}

        module_object = ModuleImplementation()
        response = module_object.post(request)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))

    @patch("core_parser_app.tools.modules.views.module.AbstractModule.render_template")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    @patch("core_parser_app.components.data_structure_element.api.upsert")
    def test_post_returns_http_response(
        self,
        mock_data_structure_element_upsert,
        mock_data_structure_element_get_by_id,
        mock_render_template,
    ):
        mock_request = Mock(spec=HttpRequest)
        mock_request.POST = {
            "module_id": "1",
        }
        mock_request.user = create_mock_user("1")

        module_object = ModuleImplementation()

        mock_data_structure_element = _create_mock_data_structure_element()
        mock_data_structure_element_get_by_id.return_value = mock_data_structure_element
        mock_data_structure_element_upsert.return_value = mock_data_structure_element
        mock_render_template.return_value = ""

        response = module_object.post(mock_request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch("core_parser_app.tools.modules.views.module.AbstractModule.render_template")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    @patch("core_parser_app.components.data_structure_element.api.upsert")
    def test_post_data_structure_element_contains_module_values(
        self,
        mock_data_structure_element_upsert,
        mock_data_structure_element_get_by_id,
        mock_render_template,
    ):
        mock_module_template = "mock_module_template"
        mock_request = Mock(spec=HttpRequest)
        mock_request.POST = {
            "module_id": "1",
        }
        mock_request.user = create_mock_user("1")

        module_object = ModuleImplementation()

        mock_data_structure_element = _create_mock_data_structure_element()
        mock_data_structure_element_get_by_id.return_value = mock_data_structure_element
        mock_data_structure_element_upsert.return_value = mock_data_structure_element
        mock_render_template.return_value = mock_module_template

        response = module_object.post(mock_request)
        response_html = json.loads(response.content)["html"]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_html, mock_module_template)


def _create_mock_data_structure_element():
    """
    Returns a mock data structure element
    :return:
    """
    mock_element = Mock(spec=DataStructureElement)
    mock_element.user = "1"
    mock_element.tag = "tag"
    mock_element.value = "value"
    mock_element.options = {}
    mock_element.children = []
    return mock_element


class ModuleImplementation(AbstractModule):
    def _render_module(self, request):
        return "module content"

    def _retrieve_data(self, request):
        return "module result"

    def _render_data(self, request):
        return "module display"


class ModuleImplementationNone(AbstractModule):
    def _render_module(self, request):
        return None

    def _retrieve_data(self, request):
        return None

    def _render_data(self, request):
        return None
