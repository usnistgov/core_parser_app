"""XML Renderer class
"""

import logging
import numbers
from os.path import join

from django.template import loader

from xml_utils.xsd_tree.operations.xml_entities import XmlEntities
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from core_parser_app.settings import AUTO_ESCAPE_XML_ENTITIES
from core_parser_app.tools.parser.exceptions import RendererError
from core_parser_app.tools.parser.renderer import DefaultRenderer

logger = logging.getLogger(__name__)


class AbstractXmlRenderer(DefaultRenderer):
    """Abstract XML renderer class"""

    def __init__(self, xsd_data):
        """Initializes XML renderer object

        Args:
            xsd_data:
        """
        xml_renderer_path = join("renderer", "xml")

        templates = {
            "xml": loader.get_template(join(xml_renderer_path, "element.html"))
        }

        super().__init__(xsd_data, templates)

    def _render_xml(self, name, attributes, content):
        """Renders form as XML

        Args:
            name:
            attributes:
            content:

        Returns:

        """
        data = {"name": name, "attributes": attributes, "content": content}

        return self._load_template("xml", data)


class XmlRenderer(AbstractXmlRenderer):
    """XML Renderer class"""

    def __init__(self, xsd_data, request):
        """Initializes XML renderer object

        Args:
            xsd_data:
        """
        super().__init__(xsd_data)
        self.request = request
        self.isRoot = True

    def render(self):
        """Renders form as XML

        Returns:

        """
        if self.data.tag == "element":
            return self.render_element(self.data)
        if self.data.tag == "choice":
            content = self.render_choice(self.data)
            root = self.data.children.all().order_by("pk")[0]
            root_elem_id = root.value
            root_elem = data_structure_element_api.get_by_id(
                root_elem_id, self.request
            )
            root_name = root_elem.options["name"]

            if (
                content[0] == ""
            ):  # Multi-root with element (no need for an element wrapper)
                return content[1]
            # Multi-root with complexType
            if (
                "xmlns" in root_elem.options
                and root_elem.options["xmlns"] is not None
            ):
                xml_ns = ' xmlns="{}"'.format(root_elem.options["xmlns"])
                content[0] += xml_ns
            return self._render_xml(root_name, content[0], content[1])

        message = "render: " + self.data.tag + " not handled"
        self.warnings.append(message)
        return ""

    def _get_parent_element(self, element):
        """Gets the parent element (with tag element, not the direct parent)
        of the current element.

        Args:
            element:

        Returns:

        """
        try:
            parent = element.parent

            while parent.tag != "element":
                parent = parent.parent

            return parent
        except Exception as e:
            logger.warning(
                "Exception caught while running 'XMLRenderer._get_parent_element': %s",
                {str(e)},
            )
            return None

    def render_element(self, element):
        """Renders an element

        Args:
            element:

        Returns:

        """
        xml_string = ""
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children.all().order_by("pk"):
            if child.tag == "elem-iter":
                children[child.pk] = child.children.all().order_by("pk")
                child_keys.append(child.pk)

                if child.children.count() > 0:
                    children_number += 1
            else:
                message = (
                    "render_element (iteration): " + child.tag + " not handled"
                )
                self.warnings.append(message)

        element_name = element.options["name"]

        for child_key in child_keys:
            for child in children[child_key]:
                content = ["", "", ""]

                # add XML Schema instance prefix if root
                if self.isRoot:
                    xsi = ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                    content[0] += xsi
                    self.isRoot = False

                if child.tag == "complex_type":
                    tmp_content = self.render_complex_type(child)
                    content[0] += tmp_content[0]
                    content[1] += tmp_content[1]
                    content[2] += tmp_content[2]
                elif child.tag == "input":
                    tmp_content = (
                        child.value if child.value is not None else ""
                    )
                    content[1] += (
                        XmlEntities().escape_xml_entities(tmp_content)
                        if AUTO_ESCAPE_XML_ENTITIES
                        else tmp_content
                    )
                elif child.tag == "simple_type":
                    tmp_content = self.render_simple_type(child)
                    content[0] += tmp_content[0]
                    content[1] += tmp_content[1]
                    content[2] += tmp_content[2]
                elif child.tag == "module":
                    tmp_content = self.render_module(child)

                    if child.options["multiple"]:
                        content[2] += tmp_content[1]
                    else:
                        content[1] += tmp_content[1]
                else:
                    message = "render_element: " + child.tag + " not handled"
                    self.warnings.append(message)

                # namespaces
                parent = self._get_parent_element(element)
                if parent is not None:
                    if (
                        "xmlns" in element.options
                        and element.options["xmlns"] is not None
                    ):
                        if (
                            "xmlns" in parent.options
                            and element.options["xmlns"]
                            != parent.options["xmlns"]
                        ):
                            xmlns = ' xmlns="{}"'.format(
                                element.options["xmlns"]
                            )
                            content[0] += xmlns
                else:
                    if (
                        "xmlns" in element.options
                        and element.options["xmlns"] is not None
                    ):
                        xmlns = ' xmlns="{}"'.format(element.options["xmlns"])
                        content[0] += xmlns

                # content[2] has the value returned by a module (the entire
                # tag, when multiple is True)
                if content[2] != "":
                    if content[1] != "":
                        raise RendererError(
                            "ERROR: More values than expected were returned "
                            "(Module multiple)."
                        )
                    xml_string += content[2]
                else:
                    xml_string += self._render_xml(
                        element_name, content[0], content[1]
                    )

        return xml_string

    def render_attribute(self, element):
        """Renders an attribute

        Args:
            element:

        Returns:

        """
        attr_key = element.options["name"]
        attr_list = []
        children = []

        for child in element.children.all().order_by("pk"):
            if child.tag == "elem-iter":
                children += child.children.all().order_by("pk")
            else:
                message = (
                    "render_attribute (iteration): "
                    + child.tag
                    + " not handled"
                )
                self.warnings.append(message)

        for child in children:
            attr_value = ""

            if child.tag == "simple_type":
                content = self.render_simple_type(child)
                attr_value = content[1]
            elif child.tag == "input":
                attr_value = child.value if child.value is not None else ""
                if AUTO_ESCAPE_XML_ENTITIES:
                    attr_value = XmlEntities().escape_xml_entities(attr_value)
            elif child.tag == "module":
                attr_value = self.render_module(child)[1]
            else:
                message = "render_attribute: " + child.tag + " not handled"
                self.warnings.append(message)

            # namespaces
            if (
                "xmlns" in element.options
                and element.options["xmlns"] is not None
            ):
                # check that element isn't declaring the same namespace xmlns=""
                parent = self._get_parent_element(element)
                xmlns = ""
                if parent is not None:
                    if (
                        "xmlns" in parent.options
                        and parent.options["xmlns"] is not None
                        and parent.options["xmlns"] == element.options["xmlns"]
                    ):
                        xmlns = ""
                    else:  # parent element is in a different namespace
                        if element.options["xmlns"] != "":
                            # TODO: test ns0 not taken and increment if needed
                            ns_prefix = (
                                element.options["ns_prefix"]
                                if element.options["ns_prefix"] is not None
                                else "ns0"
                            )
                            if ns_prefix != "":
                                xmlns = ' xmlns{0}="{1}"'.format(
                                    ":" + ns_prefix, element.options["xmlns"]
                                )
                                attr_key = "{0}:{1}".format(
                                    ns_prefix, attr_key
                                )
                            else:
                                xmlns = ' xmlns="{0}"'.format(
                                    element.options["xmlns"]
                                )
                        else:
                            xmlns = ""

                if isinstance(attr_value, numbers.Number):
                    attr_value = str(attr_value)

                attr_list.append(
                    xmlns + " " + attr_key + "='" + attr_value + "'"
                )

                # TODO: check that sibling attributes are not declaring the
                #  same namespaces
            else:
                attr_list.append(attr_key + '="' + attr_value + '"')

        return " ".join(attr_list)

    def render_complex_type(self, element):
        """Renders a complex type

        Args:
            element:

        Returns:

        """
        # XML content: attributes, inner content, outer content
        content = ["", "", ""]

        for child in element.children.all().order_by("pk"):
            tmp_content = ["", "", ""]

            # add XML Schema instance prefix if root
            if self.isRoot:
                xsi = ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                content[0] += xsi
                self.isRoot = False

            if child.tag == "sequence":
                tmp_content = self.render_sequence(child)
            elif child.tag == "simple_content":
                tmp_content = self.render_simple_content(child)
            elif child.tag == "complex_content":
                tmp_content = self.render_complex_content(child)
            elif child.tag == "attribute":
                tmp_content[0] = self.render_attribute(child)
            elif child.tag == "choice":
                tmp_content = self.render_choice(child)
            elif child.tag == "module":
                if child.options["multiple"]:
                    tmp_content[2] = self.render_module(child)[1]
                else:
                    tmp_content[1] = self.render_module(child)[1]
            else:
                message = "render_complex_type: " + child.tag + " not handled"
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_sequence(self, element):
        """Renders a sequence

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]
        children = []

        for child in element.children.all().order_by("pk"):
            if child.tag == "sequence-iter":
                children += child.children.all().order_by("pk")
            else:
                message = (
                    "render_sequence (iteration): "
                    + child.tag
                    + " not handled"
                )
                self.warnings.append(message)

        for child in children:
            tmp_content = ["", "", ""]

            if child.tag == "element":
                tmp_content[1] += self.render_element(child)
            elif child.tag == "sequence":
                tmp_content = self.render_sequence(child)
            elif child.tag == "choice":
                tmp_content = self.render_choice(child)
            else:
                message = "render_sequence: " + child.tag + " not handled"
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_simple_content(self, element):
        """Renders a simple type

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]

        for child in element.children.all().order_by("pk"):
            tmp_content = ["", "", ""]

            if child.tag == "extension":
                tmp_content = self.render_extension(child)
            elif child.tag == "restriction":
                tmp_content = self.render_restriction(child)
            else:
                message = (
                    "render_simple_content: " + child.tag + " not handled"
                )
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_complex_content(self, element):
        """Renders a complex content

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]

        for child in element.children.all().order_by("pk"):
            tmp_content = ["", "", ""]

            if child.tag == "extension":
                tmp_content = self.render_extension(child)
            elif child.tag == "restriction":
                tmp_content = self.render_restriction(child)
            else:
                message = (
                    "render_complex_content: " + child.tag + " not handled"
                )
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_choice(self, element):
        """Renders a choice

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]
        children = {}
        child_keys = []
        choice_values = {}

        for child in element.children.all().order_by("pk"):
            if child.tag == "choice-iter":
                children[child.pk] = child.children.all().order_by("pk")
                child_keys.append(child.pk)
                choice_values[child.pk] = child.value
            else:
                message = (
                    "render_choice (iteration): " + child.tag + " not handled"
                )
                self.warnings.append(message)

        for iter_element in child_keys:
            for child in children[iter_element]:
                tmp_content = ["", "", ""]

                # FIXME change orders of conditions
                if child.tag == "element":
                    if str(child.pk) == choice_values[iter_element]:
                        tmp_content[1] = self.render_element(child)
                elif child.tag == "sequence":
                    if str(child.pk) == choice_values[iter_element]:
                        tmp_content = self.render_sequence(child)
                elif child.tag == "simple_type":  # implicit extension
                    if str(child.pk) == choice_values[iter_element]:
                        tmp_content = self.render_simple_type(child)
                        ns_prefix = ""
                        xmlns = ""
                        if (
                            "ns_prefix" in child.options
                            and child.options["ns_prefix"] is not None
                        ):
                            parent = self._get_parent_element(child)
                            if parent is not None:
                                if (
                                    "xmlns" in parent.options
                                    and child.options["xmlns"]
                                    != parent.options["xmlns"]
                                ):
                                    ns_prefix = child.options["ns_prefix"]
                                    xmlns = ' xmlns{0}="{1}"'.format(
                                        ":" + ns_prefix, child.options["xmlns"]
                                    )
                                    ns_prefix += ":"

                        tmp_content[0] += ' xsi:type="{0}{1}" {2}'.format(
                            ns_prefix, child.options["name"], xmlns
                        )
                elif child.tag == "complex_type":  # implicit extension
                    if str(child.pk) == choice_values[iter_element]:
                        tmp_content = self.render_complex_type(child)
                        ns_prefix = ""
                        xmlns = ""
                        if (
                            "ns_prefix" in child.options
                            and child.options["ns_prefix"] is not None
                        ):
                            parent = self._get_parent_element(child)
                            if parent is not None:
                                if (
                                    "xmlns" in parent.options
                                    and child.options["xmlns"]
                                    != parent.options["xmlns"]
                                ):
                                    ns_prefix = child.options["ns_prefix"]
                                    xmlns = ' xmlns{0}="{1}"'.format(
                                        ":" + ns_prefix, child.options["xmlns"]
                                    )
                                    ns_prefix += ":"

                        tmp_content[0] += ' xsi:type="{0}{1}" {2}'.format(
                            ns_prefix, child.options["name"], xmlns
                        )
                else:
                    message = "render_choice: " + child.tag + " not handled"
                    self.warnings.append(message)

                content[0] = " ".join([content[0], tmp_content[0]]).strip()
                content[1] += tmp_content[1]
                content[2] += tmp_content[2]

        return content

    def render_simple_type(self, element):
        """Renders a simple type

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]

        for child in element.children.all().order_by("pk"):
            tmp_content = ["", "", ""]

            if child.tag == "restriction":
                tmp_content = self.render_restriction(child)
            elif child.tag == "attribute":
                tmp_content[0] = self.render_attribute(child)
            elif child.tag == "union":
                tmp_content[1] = child.value if child.value is not None else ""
            elif child.tag == "list":
                tmp_content[1] = child.value if child.value is not None else ""
            elif child.tag == "module":
                if child.options["multiple"]:
                    tmp_content[2] = self.render_module(child)[1]
                else:
                    tmp_content[1] = self.render_module(child)[1]
            elif child.tag == "choice":
                tmp_content = self.render_choice(child)
            else:
                message = "render_simple_type: " + child.tag + " not handled"
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_restriction(self, element):
        """Renders a restriction

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]
        value = element.value

        for child in element.children.all().order_by("pk"):
            tmp_content = ["", "", ""]

            if child.tag == "enumeration":
                tmp_content[1] = value if value is not None else ""
                if AUTO_ESCAPE_XML_ENTITIES:
                    tmp_content[1] = XmlEntities().escape_xml_entities(
                        tmp_content[1]
                    )
                value = None  # Avoid to copy the value several times
            elif child.tag == "input":
                tmp_content[1] = child.value if child.value is not None else ""
                if AUTO_ESCAPE_XML_ENTITIES:
                    tmp_content[1] = XmlEntities().escape_xml_entities(
                        tmp_content[1]
                    )
            elif child.tag == "simple_type":
                tmp_content = self.render_simple_type(child)
            else:
                message = "render_restriction: " + child.tag + " not handled"
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_extension(self, element):
        """Renders an extension

        Args:
            element:

        Returns:

        """
        content = ["", "", ""]

        for child in element.children.all().order_by("pk"):
            tmp_content = ["", "", ""]

            if child.tag == "input":
                tmp_content[1] = child.value if child.value is not None else ""
                if AUTO_ESCAPE_XML_ENTITIES:
                    tmp_content[1] = XmlEntities().escape_xml_entities(
                        tmp_content[1]
                    )
            elif child.tag == "attribute":
                tmp_content[0] = self.render_attribute(child)
            elif child.tag == "simple_type":
                tmp_content = self.render_simple_type(child)
            elif child.tag == "complex_type":
                tmp_content = self.render_complex_type(child)
            else:
                message = "render_extension: " + child.tag + " not handled"
                self.warnings.append(message)

            content[0] = " ".join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]
            content[2] += tmp_content[2]

        return content

    def render_module(self, element):
        """Renders a module

        Args:
            element:

        Returns:

        """
        return [
            "",
            element.options["data"] if "data" in element.options else "",
        ]
