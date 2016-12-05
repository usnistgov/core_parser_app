"""Builtin classes
"""
from __future__ import division

import os

from core_parser_app.settings import MODULES_ROOT
from core_parser_app.tools.modules.module import AbstractModule
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from math import ceil

RESOURCES_PATH = os.path.join(MODULES_ROOT, 'builtin', 'resources')
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'html')
SCRIPTS_PATH = os.path.join(RESOURCES_PATH, 'js')
STYLES_PATH = os.path.join(RESOURCES_PATH, 'css')


class InputModule(AbstractModule):
    """Input module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None, disabled=False):
        """Initializes module

        :param scripts:
        :param styles:
        :param label:
        :param default_value:
        :param disabled:
        """
        scripts = [os.path.join(SCRIPTS_PATH, 'input.js')] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.default_value = default_value
        self.disabled = disabled

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'input.html')
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        if self.default_value is not None:
            params.update({"default_value": self.default_value})
            
        if self.disabled is not None:
            params.update({"disabled": self.disabled})

        return AbstractModule.render_module(template, params)


class OptionsModule(AbstractModule):
    """Options Modules
    """
    def __init__(self, scripts=list(), styles=list(), label=None, options=None, disabled=False, selected=None):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        :param options:
        :param disabled:
        :param selected:
        """
        if options is None:
            options = {}

        scripts = [os.path.join(SCRIPTS_PATH, 'options.js')] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.options = options
        self.label = label
        self.disabled = disabled
        self.selected = selected

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'options.html')
        options_html = ""

        if self.selected not in self.options.keys():
            self.selected = None

        for key, val in self.options.items():
            if self.selected is not None and key == self.selected:
                options_html += "<option value='" + key + "' selected>" + val + "</option>"
            else:
                options_html += "<option value='" + key + "'>" + val + "</option>"

        params = {"options": options_html}

        if self.label is not None:
            params.update({"label": self.label})
            
        if self.disabled is not None:
            params.update({"disabled": self.disabled})

        return AbstractModule.render_module(template, params)


class PopupModule(AbstractModule):
    """Popup module
    """
    def __init__(self, scripts=list(), styles=list(), popup_content=None, button_label='Save'):
        """Initializes the module

        :param scripts:
        :param styles:
        :param popup_content:
        :param button_label:
        """
        scripts = [os.path.join(SCRIPTS_PATH, 'popup.js')] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)
        if popup_content is None:
            raise ModuleError("'popup_content' and is required. Cannot instantiate an empty popup")

        self.popup_content = popup_content
        self.button_label = button_label

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'popup.html')
        params = {
            "popup_content": self.popup_content,
            "button_label": self.button_label
        }

        return AbstractModule.render_module(template, params)


class SyncInputModule(AbstractModule):
    """Synchronous input module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None, modclass=None, disabled=False):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        :param default_value:
        :param modclass:
        :param disabled:
        """
        scripts = [os.path.join(SCRIPTS_PATH, 'sync_input.js')] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        if modclass is None:
            raise ModuleError("'modclass' is required.")

        self.modclass = modclass
        self.label = label
        self.default_value = default_value
        self.disabled = disabled

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'sync_input.html')
        params = {'class': self.modclass}
        if self.label is not None:
            params.update({"label": self.label})
        if self.default_value is not None:
            params.update({"default_value": self.default_value})
        if self.disabled is not None:
            params.update({"disabled": self.disabled})
        return AbstractModule.render_module(template, params)


class InputButtonModule(AbstractModule):
    """Input Button module
    """
    def __init__(self, scripts=list(), styles=list(), button_label='Send', label=None, default_value=None):
        """Initializes the module

        :param scripts:
        :param styles:
        :param button_label:
        :param label:
        :param default_value:
        """
        AbstractModule.__init__(self, scripts=scripts, styles=styles)
        self.button_label = button_label
        self.label = label
        self.default_value = default_value

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'input_button.html')
        params = {"button_label": self.button_label}
        if self.label is not None:
            params.update({"label": self.label})
        if self.default_value is not None:
            params.update({"default_value": self.default_value})
        return AbstractModule.render_module(template, params)


class TextAreaModule(AbstractModule):
    """Text Area module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, data=''):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        :param data:
        """
        scripts = [os.path.join(SCRIPTS_PATH, 'textarea.js')] + scripts
        styles = [os.path.join(STYLES_PATH, 'textarea.css')] + styles
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label
        self.data = data

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'textarea.html')

        params = {"label": self.label,
                  'data': self.data}

        return AbstractModule.render_module(template, params)


class AutoCompleteModule(AbstractModule):
    """ AutoCompleteModule class
    """

    def __init__(self, scripts=list(), styles=list(), label=None):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        """
        scripts = [os.path.join(SCRIPTS_PATH, 'autocomplete.js')] + scripts
        AbstractModule.__init__(self, scripts=scripts, styles=styles)

        self.label = label

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """
        template = os.path.join(TEMPLATES_PATH, 'autocomplete.html')
        params = {}

        if 'data' in request.GET:
            params['value'] = request.GET['data']

        if self.label is not None:
            params.update({"label": self.label})

        return AbstractModule.render_module(template, params)

    # Unimplemented method (to be implemented by children classes)
    def _get_module(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._get_module(self, request)

    def _get_display(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._get_display(self, request)

    def _get_result(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._get_result(self, request)

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._post_display(self, request)

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        AbstractModule._post_result(self, request)


class CheckboxesModule(AbstractModule):
    """Checbox module
    """
    def __init__(self, scripts=list(), styles=list(), label=None, name=None, options=None, selected=list()):
        """Initializes the module

        :param scripts:
        :param styles:
        :param label:
        :param name:
        :param options:
        :param selected:
        """
        scripts = [os.path.join(SCRIPTS_PATH, 'checkboxes.js')] + scripts
        styles = [os.path.join(STYLES_PATH, 'checkboxes.css')] + styles
        AbstractModule.__init__(self, scripts=scripts, styles=styles)
        
        if name is None:
            raise ModuleError("The name can't be empty.")

        self.selected = selected
        self.options = options if options is not None else dict()
        self.label = label

    # FIXME: use a template to generate the HTML of the checkbox
    @staticmethod
    def _create_html_checkbox(input_key, input_value, checked=False):
        """Returns the html of the checkbox

        :param input_value:
        :param checked:
        :return:
        """
        input_tag = '<input type="checkbox" '
        if checked:
            input_tag += 'checked '
        input_tag += 'value="' + input_key + '"/> ' + input_value

        return '<span>' + input_tag + '</span>'

    def get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """

        template = os.path.join(TEMPLATES_PATH, 'checkboxes.html')

        # Compute number of items in each columns
        col_nb = 3
        opt_nb = len(self.options)
        max_item_nb = int(ceil(opt_nb / col_nb))

        # Parameters initialization
        params = {
            "column1": "",
            "column2": "",
            "column3": "",
        }
        item_nb = 0
        col_id = 1
        checkboxes_html = ""

        # Filling the parameters
        for key, val in self.options.items():
            if item_nb == max_item_nb:
                params['column' + str(col_id)] = checkboxes_html

                checkboxes_html = ""
                item_nb = 0
                col_id += 1

            checkboxes_html += CheckboxesModule._create_html_checkbox(key, val, checked=(key in self.selected))
            item_nb += 1

        params['column' + str(col_id)] = checkboxes_html

        if self.label is not None:
            params.update({"label": self.label})

        return AbstractModule.render_module(template, params)


class AutoKeyModule(SyncInputModule):
    """Auto Key module
    """

    def __init__(self, generateKey=None):
        """Initializes the module

        :param generateKey:
        """
        if generateKey is None:
            raise ModuleError('A function for the generation of the keys should be provided (generateKey is None).')

        self.generateKey = generateKey
        SyncInputModule.__init__(self, modclass='mod_auto_key', disabled=True)

    def _get_module(self, request):
        """Returns the module

        :param request:
        :return:
        """

        # get the name of the key
        module_id = request.GET['module_id']
        module = data_structure_element_api.get_by_id(module_id)
        keyId = module.options['params']['key']

        # register the module id in the structure
        if str(module_id) not in request.session['keys'][keyId]['module_ids']:
            request.session['keys'][keyId]['module_ids'].append(str(module_id))

        # get the list of values for this key
        values = []
        modules_ids = request.session['keys'][keyId]['module_ids']
        for key_module_id in modules_ids:
            key_module = data_structure_element_api.get_by_id(key_module_id)
            if key_module.options['data'] is not None:
                values.append(key_module.options['data'])

        # if data are present
        if 'data' in request.GET:
            # set the key coming from data
            key = request.GET['data']
        else:
            # generate a unique key
            key = self.generateKey(values)
        # set the value of the module with the key
        self.default_value = key

        return SyncInputModule.get_module(self, request)

    def _get_display(self, request):
        """

        :param request:
        :return:
        """
        return ''

    def _get_result(self, request):
        """

        :param request:
        :return:
        """
        if 'data' in request.GET:
            return request.GET['data']
        return self.default_value

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        pass

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        pass
