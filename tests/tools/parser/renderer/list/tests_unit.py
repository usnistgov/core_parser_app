"""Unit tests for AbstractListRenderer class."""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.tools.parser.renderer.list import (
    AbstractListRenderer,
    ListRenderer,
)
from core_parser_app.tools.parser.renderer.xml import XmlRenderer
from core_parser_app.tools.parser.parser import XSDParser, import_xml_tree
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestAbstractListRendererRenderUl(TestCase):
    """Unit tests for `AbstractListRenderer._render_ul` method."""

    def setUp(self) -> None:
        """setUp"""
        self.renderer = AbstractListRenderer(
            MagicMock(spec=DataStructureElement)
        )
        self.mock_kwargs = {
            "content": "mock_content",
            "element_id": "mock_element_id",
            "is_hidden": True,
        }

    def test_element_id_not_str_raises_type_error(self):
        """test_element_id_not_str_raises_type_error"""
        self.mock_kwargs["element_id"] = 42  # noqa

        with self.assertRaises(TypeError):
            self.renderer._render_ul(**self.mock_kwargs)

    def test_is_hidden_not_bool_raises_type_error(self):
        """test_is_hidden_not_bool_raises_type_error"""
        self.mock_kwargs["is_hidden"] = "mock_is_hidden"  # noqa

        with self.assertRaises(TypeError):
            self.renderer._render_ul(**self.mock_kwargs)

    def test_successful_execution_returns_load_template(self):
        """test_successful_execution_returns_load_template"""
        self.assertEqual(
            self.renderer._render_ul(**self.mock_kwargs),
            self.renderer._load_template("ul", self.mock_kwargs),
        )


class TestRenderSimpleTypeXmlEscaping(TestCase):
    """Unit tests for the `XmlRenderer.render_simple_type` method"""

    def setUp(self) -> None:
        """setUp"""
        self.mock_element = MagicMock(spec=DataStructureElement)
        self.mock_request = MagicMock()
        self.renderer = XmlRenderer(self.mock_element, self.mock_request)

    def test_render_simple_type_union_escapes_entities(self):
        """test_render_simple_type_union_escapes_entities"""

        mock_child = MagicMock()
        mock_child.tag = "union"
        mock_child.value = "value & more"

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_child
        ]

        result = self.renderer.render_simple_type(self.mock_element)

        self.assertEqual(result[1], "value &amp; more")

    def test_render_simple_type_list_escapes_entities(self):
        """test_render_simple_type_list_escapes_entities"""
        mock_child = MagicMock()
        mock_child.tag = "list"
        mock_child.value = "list < value"

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_child
        ]

        result = self.renderer.render_simple_type(self.mock_element)

        self.assertEqual(result[1], "list &lt; value")

    def test_render_simple_type_handles_none_value(self):
        """test_render_simple_type_handles_none_value"""
        mock_child = MagicMock()
        mock_child.tag = "union"
        mock_child.value = None

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_child
        ]

        result = self.renderer.render_simple_type(self.mock_element)

        self.assertEqual(result[1], "")

    def test_render_simple_type_return_same_value_if_nothing_to_escape(self):
        """test_render_simple_type_return_same_value_if_nothing_to_escape"""
        mock_child = MagicMock()
        mock_child.tag = "union"
        mock_child.value = "some value"

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_child
        ]

        result = self.renderer.render_simple_type(self.mock_element)

        self.assertEqual(result[1], "some value")


class TestRendererEscaping(TestCase):
    """Unit tests for escape() calls in ListRenderer labels"""

    def setUp(self) -> None:
        """setUp"""
        self.mock_element = MagicMock(spec=DataStructureElement)
        self.mock_request = MagicMock()

        self.renderer = ListRenderer(self.mock_element, self.mock_request)

    def test_render_element_escapes_label(self):
        """test_render_element_escapes_label"""
        self.mock_element.options = {
            "name": "test_elem",
            "label": "element & test <value>",
        }
        self.mock_element.pk = 1

        mock_iter = MagicMock()
        mock_iter.tag = "elem-iter"
        mock_iter.pk = 1
        mock_iter.children.count.return_value = 0
        inner_queryset = MagicMock()
        inner_queryset.all.return_value.order_by.return_value = []
        mock_iter.children.all.return_value.order_by.return_value = (
            inner_queryset
        )

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_iter
        ]

        result = self.renderer.render_element(self.mock_element)
        self.assertIn("element &amp; test &lt;value&gt;", result)

    def test_render_attribute_escapes_label(self):
        """test_render_attribute_escapes_label"""
        self.mock_element.options = {
            "name": "test_attr",
            "label": "value < 100 & test > 0",
        }
        self.mock_element.pk = 2

        mock_iter = MagicMock()
        mock_iter.tag = "elem-iter"
        mock_iter.pk = 1
        mock_iter.children.count.return_value = 0
        inner_queryset = MagicMock()
        inner_queryset.all.return_value.order_by.return_value = []
        mock_iter.children.all.return_value.order_by.return_value = (
            inner_queryset
        )

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_iter
        ]

        result = self.renderer.render_attribute(self.mock_element)
        self.assertIn("value &lt; 100 &amp; test &gt; 0", result)

    def test_render_choice_escapes_label(self):
        """test_render_choice_escapes_label"""
        self.mock_element.options = {"label": "element <value & test>"}
        self.mock_element.pk = 3

        mock_iter = MagicMock()
        mock_iter.tag = "choice-iter"
        mock_iter.pk = 1
        mock_iter.value = "99"
        mock_iter.children.count.return_value = 0
        inner_queryset = MagicMock()
        inner_queryset.all.return_value.order_by.return_value = []
        mock_iter.children.all.return_value.order_by.return_value = (
            inner_queryset
        )

        self.mock_element.children.all.return_value.order_by.return_value = [
            mock_iter
        ]

        result = self.renderer.render_choice(self.mock_element)
        self.assertIn("element &lt;value &amp; test&gt;", result)


class TestRenderModule(TestCase):
    """Unit tests for the `ListRenderer.render_module` method"""

    def setUp(self) -> None:
        """setUp"""
        self.mock_element = MagicMock(spec=DataStructureElement)
        self.mock_request = MagicMock()
        self.renderer = ListRenderer(self.mock_element, self.mock_request)

    @patch("core_parser_app.tools.parser.renderer.list.module_api")
    @patch("core_parser_app.tools.parser.renderer.list.AbstractModule")
    def test_render_module_main_function(
        self, MockAbstractModule, MockModuleApi
    ):
        """test_render_module_main_function"""
        self.mock_element.pk = 123
        self.mock_element.options = {
            "url": "module",
            "xpath": {"xsd": "xsd/path", "xml": "xml/path"},
            "data": None,
            "attributes": None,
        }

        mock_module = MagicMock()
        mock_module.view = "path.to.view"
        MockModuleApi.get_by_url.return_value = mock_module

        mock_view_instance = MagicMock()
        MockAbstractModule.get_view_from_view_path.return_value = MagicMock(
            return_value=mock_view_instance
        )

        mock_response = MagicMock()
        mock_response.content.decode.return_value = "module html content"
        mock_view_instance._get.return_value = mock_response

        result = self.renderer.render_module(self.mock_element)

        self.assertEqual(result, "module html content")
        self.assertEqual(self.mock_request.method, "GET")
        self.assertEqual(self.mock_request.GET["module_id"], 123)
        self.assertEqual(self.mock_request.GET["url"], "module")

    @patch("core_parser_app.tools.parser.renderer.list.module_api")
    @patch("core_parser_app.tools.parser.renderer.list.AbstractModule")
    def test_render_module_with_data_and_attributes(
        self, MockAbstractModule, MockModuleApi
    ):
        """test_render_module_with_data_and_attributes"""
        self.mock_element.options = {
            "url": "module",
            "xpath": {"xsd": "xsd", "xml": "xml"},
            "data": "some_data",
            "attributes": "some_attrs",
        }

        MockModuleApi.get_by_url.return_value = MagicMock()
        mock_view_instance = MagicMock()
        MockAbstractModule.get_view_from_view_path.return_value = MagicMock(
            return_value=mock_view_instance
        )
        mock_view_instance._get.return_value = MagicMock(content=b"html")

        self.renderer.render_module(self.mock_element)

        self.assertEqual(self.mock_request.GET["data"], "some_data")
        self.assertEqual(self.mock_request.GET["attributes"], "some_attrs")

    @patch("core_parser_app.tools.parser.renderer.list.module_api")
    @patch("core_parser_app.tools.parser.renderer.list.AbstractModule")
    def test_render_module_ignores_none_data_attributes(
        self, MockAbstractModule, MockModuleApi
    ):
        """test_render_module_ignores_none_data_attributes"""
        self.mock_element.options = {
            "url": "module",
            "xpath": {"xsd": "xsd", "xml": "xml"},
            "data": None,
            "attributes": None,
        }

        MockModuleApi.get_by_url.return_value = MagicMock()
        mock_view_instance = MagicMock()
        MockAbstractModule.get_view_from_view_path.return_value = MagicMock(
            return_value=mock_view_instance
        )
        mock_view_instance._get.return_value = MagicMock(content=b"html")

        self.renderer.render_module(self.mock_element)

        self.assertNotIn("data", self.mock_request.GET)
        self.assertNotIn("attributes", self.mock_request.GET)


class TestParserUrlValidation(TestCase):
    """Unit tests for URL validation in the Parser class"""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_user = create_mock_user(user_id="1", is_superuser=True)
        self.mock_request.user = self.mock_user
        self.parser = XSDParser(
            download_dependencies=True, request=self.mock_request
        )

    @patch("core_parser_app.tools.parser.parser.url_validation")
    @patch("core_parser_app.tools.parser.parser.send_get_request")
    @patch("xml_utils.xsd_tree.xsd_tree.XSDTree.build_tree")
    def test_import_xml_tree_valid_url(self, mock_build, mock_get, mock_val):
        """test_import_xml_tree_valid_url"""
        mock_el = MagicMock()
        mock_el.attrib = {"schemaLocation": "http://localhost/schema.xsd"}
        mock_get.return_value.content = "<xml>content</xml>"
        mock_val.return_value = True

        import_xml_tree(mock_el, download_enabled=True)

        # Assert
        mock_val.assert_called_with("http://localhost/schema.xsd")
        mock_get.assert_called()

    @patch("core_parser_app.tools.parser.parser.url_validation")
    def test_import_xml_tree_invalid_url_raises(self, mock_val):
        """test_import_xml_tree_invalid_url_raises"""
        mock_val.side_effect = Exception("Invalid URL")

        mock_el = MagicMock()
        mock_el.attrib = {"schemaLocation": "invalid-url"}

        with self.assertRaises(Exception):
            import_xml_tree(mock_el, download_enabled=True)

    @patch("core_parser_app.tools.parser.parser.url_validation")
    @patch("core_parser_app.tools.parser.parser.send_get_request")
    @patch("xml_utils.xsd_tree.xsd_tree.XSDTree.build_tree")
    @patch("xml_utils.xsd_tree.xsd_tree.XSDTree.tostring")
    @patch("core_parser_app.tools.parser.parser.XSDFlattenerDatabaseOrURL")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    def test_generate_element_absent_valid_url(
        self,
        mock_get_id,
        MockFlattener,
        mock_to_string,
        mock_build,
        mock_get,
        mock_val,
    ):
        """test_generate_element_absent_valid_url"""
        mock_flattener_instance = MockFlattener.return_value
        mock_flattener_instance.get_flat.return_value = (
            "<xml>flattened_content</xml>"
        )
        mock_to_string.return_value = "<xml>mock_xsd_content</xml>"

        mock_sub_element = MagicMock(spec=DataStructureElement)
        mock_sub_element.parent = MagicMock(spec=DataStructureElement)
        mock_sub_element.parent.options = {
            "schema_location": "http://localhost/schema.xsd",
            "xpath": {"xsd": "/xs:schema/xs:element", "xml": "/root/element"},
        }
        mock_get_id.return_value = mock_sub_element

        mock_val.return_value = True
        mock_get.return_value.content = "<xml>content</xml>"

        with patch(
            "core_parser_app.tools.parser.renderer.list.ListRenderer.render",
            return_value="<html></html>",
        ), patch(
            "core_parser_app.components.data_structure_element.api.upsert"
        ), patch(
            "core_parser_app.components.data_structure_element.api.add_child"
        ), patch(
            "core_parser_app.tools.parser.parser.load_schema_data_in_db"
        ) as mock_load:

            mock_root = MagicMock(spec=DataStructureElement)
            mock_root.pk = 1
            mock_root.options = {}
            mock_load.return_value = mock_root

            self.parser.generate_element_absent(
                element_id="123", xsd_doc_data="<root/>"
            )

            mock_val.assert_called_with("http://localhost/schema.xsd")

    @patch("core_parser_app.tools.parser.parser.url_validation")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    def test_generate_element_absent_invalid_url(self, mock_get_id, mock_val):
        """test_generate_element_absent_invalid_url"""
        mock_sub_element = MagicMock(spec=DataStructureElement)
        mock_sub_element.parent = MagicMock(spec=DataStructureElement)
        mock_sub_element.parent.options = {"schema_location": "bad-url"}
        mock_get_id.return_value = mock_sub_element

        mock_val.side_effect = Exception("Invalid URL")

        with self.assertRaises(Exception):
            self.parser.generate_element_absent(
                element_id="123", xsd_doc_data="<root/>"
            )

    @patch("core_parser_app.tools.parser.parser.url_validation")
    @patch("core_parser_app.tools.parser.parser.send_get_request")
    @patch("xml_utils.xsd_tree.xsd_tree.XSDTree.build_tree")
    @patch("xml_utils.xsd_tree.xsd_tree.XSDTree.tostring")
    @patch("core_parser_app.tools.parser.parser.XSDFlattenerDatabaseOrURL")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    def test_generate_choice_absent_valid_url(
        self,
        mock_get_id,
        MockFlattener,
        mock_to_string,
        mock_build,
        mock_get,
        mock_val,
    ):
        """test_generate_choice_absent_valid_url"""
        mock_flattener_instance = MockFlattener.return_value
        mock_flattener_instance.get_flat.return_value = (
            "<xml>flattened_content</xml>"
        )
        mock_to_string.return_value = "<xml>mock_xsd_content</xml>"

        # Setup element as a 'choice'
        mock_element = MagicMock(spec=DataStructureElement)
        mock_element.tag = "element"
        mock_element.options = {
            "schema_location": "http://localhost/choice_schema.xsd",
            "xpath": {"xsd": "/xs:schema/xs:choice", "xml": "/root/choice"},
        }
        mock_get_id.return_value = mock_element

        mock_val.return_value = True
        mock_get.return_value.content = "<xml>content</xml>"

        with patch(
            "core_parser_app.tools.parser.renderer.list.ListRenderer.render",
            return_value="<html></html>",
        ), patch(
            "core_parser_app.components.data_structure_element.api.upsert"
        ), patch(
            "core_parser_app.components.data_structure_element.api.add_child"
        ), patch(
            "core_parser_app.tools.parser.parser.load_schema_data_in_db"
        ) as mock_load:

            mock_root = MagicMock(spec=DataStructureElement)
            mock_root.pk = 1
            mock_root.options = {}
            mock_load.return_value = mock_root

            self.parser.generate_choice_absent(
                element_id="123", xsd_doc_data="<root/>"
            )

            mock_val.assert_called_with("http://localhost/choice_schema.xsd")

    @patch("core_parser_app.tools.parser.parser.url_validation")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    def test_generate_choice_absent_invalid_url(self, mock_get_id, mock_val):
        """test_generate_choice_absent_invalid_url"""
        mock_element = MagicMock(spec=DataStructureElement)
        mock_element.options = {"schema_location": "bad-url"}
        mock_get_id.return_value = mock_element

        mock_val.side_effect = Exception("Invalid URL")

        with self.assertRaises(Exception):
            self.parser.generate_choice_absent(
                element_id="123", xsd_doc_data="<root/>"
            )
