""" tests unit
"""

from unittest.case import TestCase
from unittest.mock import Mock, patch

from django.core import exceptions as django_exceptions

from core_main_app.commons.exceptions import DoesNotExist, XSDError
from core_main_app.components.template.models import Template
from core_parser_app.components.module import api as module_api
from core_parser_app.components.module.models import Module


class TestModuleGetById(TestCase):
    """Test Module Get By Id"""

    @patch("core_parser_app.components.module.models.Module.get_by_id")
    def test_module_get_by_id_returns_module(self, mock_get_by_id):
        """test_module_get_by_id_returns_module"""

        # Arrange
        mock_module = _create_mock_module()

        mock_get_by_id.return_value = mock_module

        # Act
        result = module_api.get_by_id(mock_module.id)

        # Assert
        self.assertIsInstance(result, Module)

    @patch("core_parser_app.components.module.models.Module.get_by_id")
    def test_module_get_by_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test_module_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = -1
        mock_get_by_id.side_effect = DoesNotExist("")

        # Act + Assert
        with self.assertRaises(DoesNotExist):
            module_api.get_by_id(mock_absent_id)


class TestModuleGetByUrl(TestCase):
    """Test Module Get By Url"""

    @patch("core_parser_app.components.module.models.Module.get_by_url")
    def test_module_get_by_url_returns_module(self, mock_get_by_url):
        """test_module_get_by_url_returns_module"""

        # Arrange
        mock_module = _create_mock_module()

        mock_get_by_url.return_value = mock_module

        # Act
        result = module_api.get_by_url(mock_module.url)

        # Assert
        self.assertIsInstance(result, Module)

    @patch("core_parser_app.components.module.models.Module.get_by_url")
    def test_module_get_by_url_raises_exception_if_object_does_not_exist(
        self, mock_get_by_url
    ):
        """test_module_get_by_url_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_url = "/absent"
        mock_get_by_url.side_effect = DoesNotExist("")

        # Act + Assert
        with self.assertRaises(DoesNotExist):
            module_api.get_by_url(mock_absent_url)


class TestModuleGetAll(TestCase):
    """Test Module Get All"""

    @patch("core_parser_app.components.module.models.Module.get_all")
    def test_module_list_contains_only_module(self, mock_get_all):
        """test_module_list_contains_only_module"""

        # Arrange
        mock_module_1 = _create_mock_module()
        mock_module_2 = _create_mock_module()
        mock_get_all.return_value = [mock_module_1, mock_module_2]

        # Act
        result = module_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, Module) for item in result))


class TestModuleUpsert(TestCase):
    """Test Module Upsert"""

    @patch("core_parser_app.components.module.models.Module.save")
    def test_module_upsert_valid_returns_module(self, mock_save):
        """test_module_upsert_valid_returns_module"""

        module = _create_module()

        mock_save.return_value = module
        result = module_api.upsert(module)
        self.assertIsInstance(result, Module)

    @patch("core_parser_app.components.module.models.Module.save")
    def test_module_upsert_invalid_raises_validation_error(self, mock_save):
        """test_module_upsert_invalid_raises_validation_error"""

        module = _create_module()
        mock_save.side_effect = django_exceptions.ValidationError("")
        with self.assertRaises(django_exceptions.ValidationError):
            module_api.upsert(module)


class TestModuleGetAllUrls(TestCase):
    """Test Module Get All Urls"""

    @patch("core_parser_app.components.module.models.Module.get_all_urls")
    def test_module_list_contains_only_urls(self, mock_get_all_urls):
        """test_module_list_contains_only_urls"""

        # Arrange
        mock_module_1 = _create_mock_module()
        mock_module_2 = _create_mock_module()
        mock_get_all_urls.return_value = [mock_module_1.url, mock_module_2.url]

        # Act
        result = module_api.get_all_urls()

        # Assert
        self.assertTrue(all(isinstance(item, str) for item in result))


class TestAddModule(TestCase):
    """Test Add Module"""

    def test_add_module_raises_xsd_error_if_wrong_template_format(self):
        """test_add_module_raises_xsd_error_if_wrong_template_format"""

        # Arrange
        json_template = _get_json_template()

        # Act + Assert
        with self.assertRaises(XSDError):
            module_api.add_module(json_template, 1, "xpath", request=None)


class TestDeleteModule(TestCase):
    """Test Delete Module"""

    def test_delete_module_raises_xsd_error_if_wrong_template_format(self):
        """test_delete_module_raises_xsd_error_if_wrong_template_format"""

        # Arrange
        json_template = _get_json_template()

        # Act + Assert
        with self.assertRaises(XSDError):
            module_api.delete_module(json_template, 1, "xpath")


def _create_module():
    """Returns a module

    Returns:

    """
    return Module(id=1, name="module", url="/module", view="Module.view")


def _create_mock_module():
    """
    Returns a mock module
    :return:
    """
    mock_module = Mock(spec=Module)
    mock_module.name = "module"
    mock_module.url = "/module"
    mock_module.view = "Module.view"
    mock_module.id = 1
    return mock_module


def _get_json_template():
    """Get JSON template

    Returns:

    """
    template = Template()
    template.format = Template.JSON
    template.id_field = 1
    template.content = "{}"
    return template
