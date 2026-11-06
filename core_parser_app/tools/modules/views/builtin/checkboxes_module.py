"""Checkboxes Module"""

from abc import ABCMeta

from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.views.module import AbstractModule


class AbstractCheckboxesModule(AbstractModule, metaclass=ABCMeta):
    """Checkboxes module"""

    def __init__(
        self,
        scripts=None,
        styles=None,
        label=None,
        name=None,
        options=None,
        selected=None,
    ):
        """Initialize the module

        Args:
            scripts:
            styles:
            label:
            name:
            options:
            selected:
        """

        module_scripts = ["core_parser_app/js/builtin/checkboxes.js"]
        if scripts:
            module_scripts += scripts
        module_styles = ["core_parser_app/css/builtin/checkboxes.css"]
        if styles:
            module_styles += styles
        AbstractModule.__init__(
            self, scripts=module_scripts, styles=module_styles
        )

        if name is None:
            raise ModuleError("The name can't be empty.")

        self.selected = selected
        self.options = options if options is not None else dict()
        self.label = label

    def _render_module(self, request):
        """Return the module

        Args:
            request:

        Returns:

        """
        # Compute number of items in each columns
        col_nb = 3

        # Parameters initialization
        columns = [[] for _ in range(col_nb)]

        for i, (key, val) in enumerate(self.options.items()):
            col_id = i % col_nb
            columns[col_id].append(
                {
                    "key": key,
                    "val": val,
                    "checked": (
                        key in self.selected if self.selected else False
                    ),
                }
            )

        params = {"columns": columns}

        if self.label is not None:
            params.update({"label": self.label})

        return AbstractModule.render_template(
            "core_parser_app/builtin/checkboxes.html", params
        )
