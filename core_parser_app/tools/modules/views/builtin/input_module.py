""" Input Module
"""
from abc import ABCMeta

from core_parser_app.tools.modules.views.module import AbstractModule


class AbstractInputModule(AbstractModule, metaclass=ABCMeta):
    """Input module"""

    def __init__(
        self,
        scripts=list(),
        styles=list(),
        label=None,
        default_value=None,
        disabled=False,
        placeholder=None,
    ):
        """Initialize the module

        Args:
            scripts:
            styles:
            label:
            default_value:
            disabled:
            placeholder:
        """
        scripts = ["core_parser_app/js/builtin/input.js"] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.default_value = default_value
        self.disabled = disabled
        self.placeholder = placeholder

    def _render_module(self, request):
        """Return module's rendering

        Args:
            request:

        Returns:

        """
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        if self.default_value is not None:
            params.update({"default_value": self.default_value})

        if self.disabled is not None:
            params.update({"disabled": self.disabled})

        if self.placeholder is not None:
            params.update({"placeholder": self.placeholder})

        return AbstractModule.render_template(
            "core_parser_app/builtin/input.html", params
        )
