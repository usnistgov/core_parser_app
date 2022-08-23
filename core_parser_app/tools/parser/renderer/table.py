"""Table Renderer class
"""
from __future__ import print_function

import logging
from os.path import join

from django.template import loader

from core_parser_app.tools.parser.renderer import DefaultRenderer

logger = logging.getLogger(__name__)


class AbstractTableRenderer(DefaultRenderer):
    """Abstract Table Renderer"""

    def __init__(self, xsd_data):
        """Initializes table renderer object

        Args:
            xsd_data:
        """
        table_renderer_path = join("renderer", "table")
        table_templates = {
            "top": loader.get_template(join(table_renderer_path, "wrap.html")),
            "table": loader.get_template(join(table_renderer_path, "table.html")),
            "tr": loader.get_template(join(table_renderer_path, "tr.html")),
        }

        super().__init__(xsd_data, table_templates)

    def _render_table(self, content):
        """Renders table

        Args:
            content:

        Returns:

        """
        data = {"content": content}

        return self._load_template("table", data)

    def _render_tr(self, name, content):
        """Renders table tr element

        Args:
            name:
            content:

        Returns:

        """
        data = {"name": name, "content": content}

        return self._load_template("tr", data)

    def _render_top(self, title, content):
        """Renders table top element

        Args:
            title:
            content:

        Returns:

        """
        data = {"title": title, "content": content}

        return self._load_template("top", data)


class TableRenderer(AbstractTableRenderer):
    """Table Renderer"""

    def __init__(self, xsd_data):
        """Initializes table renderer

        Args:
            xsd_data:
        """
        super().__init__(xsd_data)

    def render(self):
        """Renders the form as a table

        Returns:

        """
        html_content = ""

        if self.data.tag == "element":
            html_content += self.render_element(self.data)
        else:
            message = "render_data: " + self.data.tag + " not handled"
            self.warnings.append(message)

        return self._render_top(self.data.options["name"], html_content)

    def render_element(self, element):
        """Renders an element

        Args:
            element:

        Returns:

        """
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children.all():
            if child.tag == "elem-iter":
                children[child.pk] = child.children.all()
                child_keys.append(child.pk)

                if child.children.count() > 0:
                    children_number += 1
            else:
                message = "render_element (iteration): " + child.tag + " not handled"
                self.warnings.append(message)

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if children_number < element.options["max"] or element.options["max"] == -1:
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)

        for child_key in child_keys:
            # FIXME Use tuples instead
            sub_elements = []
            sub_inputs = []

            for child in children[child_key]:
                if child.tag == "complex_type":
                    sub_elements.append(self.render_complex_type(child))
                    sub_inputs.append(False)
                elif child.tag == "simple_type":
                    sub_elements.append(self.render_simple_type(child))
                    sub_inputs.append(False)
                elif child.tag == "input":
                    sub_elements.append(self._render_input(child.pk))
                    sub_inputs.append(True)
                elif child.tag == "module":
                    sub_elements.append(self.render_module(child))
                    sub_inputs.append(False)
                else:
                    message = "render_element: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                # FIXME Find a way to make the label grey
                html_content = ""
            else:
                html_content = ""
                for child_index in range(len(sub_elements)):
                    if sub_inputs[child_index]:  # Element is an input
                        html_content += "%s%s%s" % (
                            element.options["name"],
                            sub_elements[child_index],
                            buttons,
                        )
                    else:  # Element is not an input
                        html_content += "%s%s%s" % (
                            self._render_collapse_button(),
                            element.options["name"],
                            buttons,
                        )

            final_html += self._render_tr(
                element["options"]["name"] + buttons, html_content
            )

        return final_html

    def render_complex_type(self, element):
        """Renders a complex type

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element["children"]:
            if child["tag"] == "sequence":
                html_content += self.render_sequence(child)
            elif child["tag"] == "simple_content":
                html_content += self.render_simple_content(child)
            elif child["tag"] == "attribute":
                html_content += self.render_attribute(child)
            else:
                logger.debug("%s not handled (render_complex_type)", child["tag"])

        return html_content

    def render_attribute(self, element):
        """Renders an attribute

        Args:
            element:

        Returns:

        """
        html_content = ""
        children = []

        for child in element["children"]:
            if child["tag"] == "elem-iter":
                children += child["children"]
            else:
                logger.debug("%s not handled (render_attribute base)", child["tag"])

        for child in children:
            if child["tag"] == "simple_type":
                html_content += self.render_simple_type(child)
            elif child["tag"] == "input":
                html_content += self._render_input(child)
            else:
                logger.debug("%s not handled (render_attribute)", child["tag"])

        return self._render_tr(element["options"]["name"], html_content)

    def render_sequence(self, element):
        """Renders a sequence

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element["children"]:
            if child["tag"] == "element":
                html_content += self.render_element(child)
            else:
                logger.debug("%s not handled (render_sequence)", child["tag"])

        return html_content

    def render_simple_content(self, element):
        """Renders a simple content

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element["children"]:
            if child["tag"] == "element":
                html_content += self.render_element(child)
            elif child["tag"] == "extension":
                html_content += self.render_extension(child)
            else:
                logger.debug("%s not handled (render_simple_content)", child["tag"])

        return html_content

    def render_simple_type(self, element):
        """Renders a simple type

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element["children"]:
            # if child["tag"] == "element":
            #     self._render_element(child)
            if child["tag"] == "restriction":
                html_content += self.render_restriction(child)
            else:
                logger.debug("%s not handled (render_simple_type)", child["tag"])

        return html_content

    def render_extension(self, element):
        """Renders an extension

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element["children"]:
            if child["tag"] == "input":
                html_content += self._render_input(child)
            elif child["tag"] == "attribute":
                html_content += self.render_attribute(child)
            else:
                logger.debug("%s not handled (render_extension)", child["tag"])

        return html_content

    def render_restriction(self, element):
        """Renders a restriction

        Args:
            element:

        Returns:

        """
        options = []
        subhtml = ""

        for child in element["children"]:
            if child["tag"] == "enumeration":
                options.append((child["value"], child["value"], False))
            elif child["tag"] == "input":
                subhtml += self._render_input(child)
            else:
                logger.debug("%s not handled (rend_ext)", child["tag"])

        if subhtml == "" or len(options) != 0:
            return self._render_select(
                element.pk, "restriction", options, element.options
            )

        return subhtml

    def render_module(self, element):
        """Renders a module

        Args:
            element:

        Returns:

        """
        return ""
