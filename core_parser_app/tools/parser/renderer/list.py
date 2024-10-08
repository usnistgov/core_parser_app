"""List Renderer class
"""

import logging
from os.path import join

from django.template import loader

from core_parser_app.components.module import api as module_api
from core_parser_app.tools.modules.views.module import AbstractModule
from core_parser_app.tools.parser.renderer import DefaultRenderer

logger = logging.getLogger(__name__)


class AbstractListRenderer(DefaultRenderer):
    """Abstract List Renderer"""

    def __init__(self, xsd_data):
        """Initializes renderer object

        Args:
            xsd_data:
        """
        list_renderer_path = join("renderer", "list")

        templates = {
            "ul": loader.get_template(join(list_renderer_path, "ul.html")),
            "li": loader.get_template(join(list_renderer_path, "li.html")),
            "attributes": loader.get_template(
                join(list_renderer_path, "attributes.html")
            ),
        }

        super().__init__(xsd_data, templates)

    def _render_ul(self, content, element_id, is_hidden=False):
        """Renders HTML ul element

        Args:
            content:
            element_id:
            is_hidden:

        Returns:

        """
        # FIXME Django SafeText type cause the test to fail
        # if type(content) not in [str, unicode]:
        #     raise TypeError('First param (content) should be a str (' + str(type(content)) +
        #     ' given)')

        # FIXME remove parameter type-checking
        if not isinstance(element_id, str) and element_id is not None:
            raise TypeError(
                "Second param (element_id) should be a str or None (%s given)"
                % str(type(element_id))
            )

        if not isinstance(is_hidden, bool):
            raise TypeError(
                "Third param (chosen) should be a bool (%s given)"
                % str(type(is_hidden))
            )

        data = {
            "content": content,
            "element_id": element_id,
            "is_hidden": is_hidden,
        }

        return self._load_template("ul", data)

    def _render_li(self, content, li_class, li_id):
        """Renders HTML li element

        Args:
            content:
            li_class:
            li_id:

        Returns:

        """
        data = {"li_class": li_class, "li_id": str(li_id), "content": content}

        return self._load_template("li", data)


class ListRenderer(AbstractListRenderer):
    """List Renderer class"""

    def __init__(self, xsd_data, request):
        """Initializes List renderer object

        Args:
            xsd_data:
            request:
        """
        super().__init__(xsd_data)
        self.request = request  # FIXME Find a way to avoid the use of request
        self.partial = False

    def render(self, partial=False):
        """Renders form as a list

        Args:
            partial:

        Returns:

        """
        html_content = ""
        self.partial = partial

        if self.data.tag == "element":
            html_content += self.render_element(self.data)
        elif self.data.tag == "attribute":
            html_content += self.render_attribute(self.data)
        elif self.data.tag == "choice":
            html_content += self.render_choice(self.data)
        elif self.data.tag == "sequence":
            html_content += self.render_sequence(self.data, partial)
        else:
            message = "render: " + self.data.tag + " not handled"
            self.warnings.append(message)

        if not partial:
            return self._render_warnings() + self._render_ul(
                html_content, str(self.data.pk)
            )

        return html_content

    def render_element(self, element):
        """Renders an element

        Args:
            element:

        Returns:

        """
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

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if (
                children_number < element.options["max"]
                or element.options["max"] == -1
            ):
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)

        element_name = element.options["name"]

        if "label" in element.options and element.options["label"] != "":
            element_name = element.options["label"]

        for child_key in child_keys:
            # FIXME Use tuples instead
            sub_elements = []
            sub_inputs = []
            sub_buttons = []

            for child in children[child_key].all().order_by("pk"):
                if child.tag == "complex_type":
                    sub_elements.append(self.render_complex_type(child))
                    sub_inputs.append(False)
                    sub_buttons.append(True)
                elif child.tag == "simple_type":
                    sub_elements.append(self.render_simple_type(child))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "input":
                    sub_elements.append(self._render_input(child))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "module":
                    sub_elements.append(self.render_module(child))
                    sub_inputs.append(False)
                    sub_buttons.append(not child.options["multiple"])
                else:
                    message = "render_element: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                html_content = element_name + buttons
                li_class = "removed"
            else:
                li_class = str(element.pk)
                html_content = ""
                for child_index in range(len(sub_elements)):
                    html_buttons = buttons

                    if not sub_buttons[child_index]:
                        html_buttons = self._render_buttons(False, del_button)

                    if sub_inputs[child_index]:
                        html_content += (
                            element_name
                            + sub_elements[child_index]
                            + html_buttons
                        )
                    else:
                        html_content += (
                            self._render_collapse_button()
                            + element_name
                            + html_buttons
                        )
                        html_content += self._render_ul(
                            sub_elements[child_index], None
                        )

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            final_html += self._render_li(html_content, li_class, child_key)

        return final_html

    def render_complex_type(self, element):
        """Renders a complex type

        Args:
            element:

        Returns:

        """
        html_content = ""

        attributes = []
        simple = False

        for child in element.children.all().order_by("pk"):
            if child.tag == "sequence":
                html_content += self.render_sequence(child)
            elif child.tag == "simple_content":
                simple = True
                html_content += self.render_simple_content(child)
            elif child.tag == "complex_content":
                html_content += self.render_complex_content(child)
            elif child.tag == "attribute":
                attributes.append(self.render_attribute(child))
            elif child.tag == "choice":
                html_content += self.render_choice(child)
            elif child.tag == "module":
                html_content += self.render_module(child)
            else:
                message = "render_complex_type: " + child.tag + " not handled"
                self.warnings.append(message)

        if len(attributes) > 0:
            html_content = self._render_list_attributes(
                attributes, html_content, simple
            )
        return html_content

    def render_attribute(self, element):
        """Renders an attribute

        Args:
            element:

        Returns:

        """
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
                    "render_attribute (iteration): "
                    + child.tag
                    + " not handled"
                )
                self.warnings.append(message)

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if (
                children_number < element.options["max"]
                or element.options["max"] == -1
            ):
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)
        element_name = element.options["name"]

        if "label" in element.options and element.options["label"] != "":
            element_name = element.options["label"]

        for child_key in child_keys:
            sub_elements = []
            sub_inputs = []
            sub_buttons = []

            for child in children[child_key].all().order_by("pk"):
                if child.tag == "simple_type":
                    sub_elements.append(self.render_simple_type(child))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "input":
                    sub_elements.append(self._render_input(child))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "module":
                    sub_elements.append(self.render_module(child))
                    sub_inputs.append(False)
                    sub_buttons.append(not child.options["multiple"])
                else:
                    message = "render_attribute: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                html_content = element_name + buttons
                li_class = "removed"
            else:
                li_class = str(element.pk)
                html_content = ""
                for child_index in range(len(sub_elements)):
                    html_buttons = buttons
                    if not sub_buttons[child_index]:
                        html_buttons = self._render_buttons(False, del_button)

                    if sub_inputs[child_index]:
                        html_content += (
                            element_name
                            + sub_elements[child_index]
                            + html_buttons
                        )
                    else:
                        html_content += (
                            self._render_collapse_button()
                            + element_name
                            + html_buttons
                        )
                        html_content += self._render_ul(
                            sub_elements[child_index], None
                        )

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            final_html += self._render_li(html_content, li_class, child_key)

        return final_html

    def render_sequence(self, element, force_full_display=False):
        """Renders a sequence

        Args:
            element:
            force_full_display:

        Returns:

        """
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children.all().order_by("pk"):
            if child.tag == "sequence-iter":
                children[child.pk] = child.children.all().order_by("pk")
                child_keys.append(child.pk)

                if child.children.count() > 0:
                    children_number += 1
            else:
                message = (
                    "render_sequence (iteration): "
                    + child.tag
                    + " not handled"
                )
                self.warnings.append(message)

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False
        empty = False

        if "max" in element.options:
            if (
                children_number < element.options["max"]
                or element.options["max"] == -1
            ):
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

            # Case of an empty sequence (no children => nb < min)
            if children_number < element.options["min"]:
                empty = True

        if empty:  # Empty sequence string (no need to go further)
            return ""

        buttons = self._render_buttons(add_button, del_button)

        for child_key in child_keys:
            # li_class = ''
            sub_elements = []
            html_content = ""

            for child in children[child_key].all().order_by("pk"):
                if child.tag == "element":
                    sub_elements.append(self.render_element(child))
                elif child.tag == "sequence":
                    sub_elements.append(self.render_sequence(child))
                elif child.tag == "choice":
                    sub_elements.append(self.render_choice(child))
                else:
                    message = "render_attribute: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                li_class = "removed"
            else:
                li_class = str(element.pk)

                for child_index in range(len(sub_elements)):
                    if (
                        children_number != 1
                        or element.options["min"] != 1
                        or force_full_display
                    ):
                        html_content += self._render_ul(
                            sub_elements[child_index], None
                        )
                    else:
                        html_content += sub_elements[child_index]

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            if (
                children_number != 1
                or element.options["min"] != 1
                or force_full_display
            ):
                final_html += self._render_li(
                    self._render_collapse_button()
                    + "Sequence "
                    + buttons
                    + html_content,
                    li_class,
                    child_key,
                )
            else:
                final_html += html_content

        return final_html

    def render_choice(self, element):
        """Renders a choice

        Args:
            element:

        Returns:

        """
        # html_content = ''
        children = {}
        child_keys = []
        choice_values = {}
        children_number = 0

        for child in element.children.all().order_by("pk"):
            if child.tag == "choice-iter":
                children[child.pk] = child.children.all().order_by("pk")
                child_keys.append(child.pk)

                if child.children.count() > 0:
                    children_number += 1

                choice_values[child.pk] = child.value
            else:
                message = (
                    "render_choice (iteration): " + child.tag + " not handled"
                )
                self.warnings.append(message)

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if (
                children_number < element.options["max"]
                or element.options["max"] == -1
            ):
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)

        final_html = ""
        item_number = 1

        for iter_element in child_keys:
            sub_content = ""
            html_content = ""
            options = []

            for child in children[iter_element].all().order_by("pk"):
                element_html = ""
                is_selected_element = (
                    str(child.pk) == choice_values[iter_element]
                )

                if child.tag == "element":
                    name = (
                        child.options["label"]
                        if "label" in child.options
                        else child.options["name"]
                    )
                    options.append((str(child.pk), name, is_selected_element))
                    element_html = self.render_element(child)
                elif child.tag == "sequence":
                    options.append(
                        (
                            str(child.pk),
                            "Sequence " + str(item_number),
                            is_selected_element,
                        )
                    )
                    item_number += 1

                    element_html = self.render_sequence(child)
                elif child.tag == "simple_type":
                    name = (
                        child.options["label"]
                        if "label" in child.options
                        else child.options["name"]
                    )
                    options.append((str(child.pk), name, is_selected_element))
                    element_html = self.render_simple_type(child)
                elif child.tag == "complex_type":
                    name = (
                        child.options["label"]
                        if "label" in child.options
                        else child.options["name"]
                    )
                    options.append((str(child.pk), name, is_selected_element))
                    element_html = self.render_complex_type(child)
                else:
                    message = "render_choice: " + child.tag + " not handled"
                    self.warnings.append(message)

                if element_html != "":
                    sub_content += self._render_ul(
                        element_html, str(child.pk), (not is_selected_element)
                    )

            label = (
                element.options["label"]
                if "label" in element.options
                else "Choice"
            )

            if children_number == 0:  # Choice has no child
                li_class = "removed"
                html_content = f"{label} {buttons}"
            else:  # Choice has children
                li_class = str(element.pk)

                # Choice contains only one element, we don't generate the select
                if children[iter_element].count() == 1:
                    html_content += options[0][1] + sub_content
                else:  # Choice contains a list
                    html_content += f"{label} {self._render_select(None, 'choice', options, element_options=element.options)}{buttons}"
                    html_content += sub_content

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            final_html += self._render_li(html_content, li_class, iter_element)

        return final_html

    def render_simple_content(self, element):
        """Renders a simple content

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element.children.all().order_by("pk"):
            if child.tag == "extension":
                html_content += self.render_extension(child)
            elif child.tag == "restriction":
                html_content += self.render_restriction(child)
            else:
                message = (
                    "render_simple_content: " + child.tag + " not handled"
                )
                self.warnings.append(message)

        return html_content

    def render_complex_content(self, element):
        """Renders a complex type

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element.children.all().order_by("pk"):
            if child.tag == "extension":
                html_content += self.render_extension(child)
            elif child.tag == "restriction":
                html_content += self.render_extension(child)
            else:
                message = (
                    "render_complex_content: " + child.tag + " not handled"
                )
                self.warnings.append(message)

        return html_content

    def render_simple_type(self, element):
        """Renders a simple type

        Args:
            element:

        Returns:

        """
        html_content = ""

        for child in element.children.all().order_by("pk"):
            if child.tag == "restriction":
                html_content += self.render_restriction(child)
            elif child.tag == "list":
                html_content += self._render_input(child)
            elif child.tag == "union":
                html_content += self._render_input(child)
            elif child.tag == "attribute":
                html_content += self.render_attribute(child)
            elif child.tag == "module":
                html_content += self.render_module(child)
            elif child.tag == "choice":
                html_content += self.render_choice(child)
            else:
                message = "render_simple_type: " + child.tag + " not handled"
                self.warnings.append(message)

        return html_content

    def render_extension(self, element):
        """Renders an extension

        Args:
            element:

        Returns:

        """
        html_content = ""

        attributes = []
        simple = True

        for child in element.children.all().order_by("pk"):
            if child.tag == "input":
                html_content += self._render_input(child)
            elif child.tag == "attribute":
                attributes.append(self.render_attribute(child))
            elif child.tag == "simple_type":
                html_content += self.render_simple_type(child)
            elif child.tag == "complex_type":
                simple = False
                html_content += self.render_complex_type(child)
            else:
                message = "render_extension: " + child.tag + " not handled"
                self.warnings.append(message)

        if len(attributes) > 0:
            html_content = self._render_list_attributes(
                attributes, html_content, simple
            )

        return html_content

    def render_restriction(self, element):
        """Renders a restriction

        Args:
            element:

        Returns:

        """
        options = []
        subhtml = ""

        for child in element.children.all().order_by("pk"):
            if child.tag == "enumeration":
                options.append(
                    (child.value, child.value, child.value == element.value)
                )
            elif child.tag == "simple_type":
                subhtml += self.render_simple_type(child)
            elif child.tag == "input":
                subhtml += self._render_input(child)
            else:
                message = "render_restriction: " + child.tag + " not handled"
                self.warnings.append(message)

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
        module_options = element.options
        module_url = module_options["url"]

        module = module_api.get_by_url(module_url)
        module_view = AbstractModule.get_view_from_view_path(
            module.view
        ).as_view()

        module_request = self.request
        module_request.method = "GET"

        module_request.GET = {
            "module_id": element.pk,
            "url": module_url,
            "xsd_xpath": module_options["xpath"]["xsd"],
            "xml_xpath": module_options["xpath"]["xml"],
        }

        # if the loaded doc has data, send them to the module for initialization
        if module_options["data"] is not None:
            module_request.GET["data"] = module_options["data"]

        if module_options["attributes"] is not None:
            module_request.GET["attributes"] = module_options["attributes"]

        # renders the module
        return module_view(module_request).content.decode("utf-8")

    def _render_list_attributes(
        self, attributes, html_content, simple_element
    ):
        """Renders attributes as a list

        Args:
            attributes:
            html_content:
            simple_element:

        Returns:

        """
        if simple_element:
            data = {"attributes_html": attributes}
            html_content += self._load_template("attributes", data)
        else:
            html_content = "".join(attributes) + html_content

        return html_content
