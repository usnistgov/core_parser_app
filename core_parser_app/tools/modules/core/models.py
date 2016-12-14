from core_parser_app.settings import MODULES_ROOT
from core_parser_app.tools.modules.builtin.models import OptionsModule
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from os.path import join

RESOURCES_PATH = join(MODULES_ROOT, 'core', 'resources')
TEMPLATES_PATH = join(RESOURCES_PATH, 'html')
SCRIPTS_PATH = join(RESOURCES_PATH, 'js')
STYLES_PATH = join(RESOURCES_PATH, 'css')


class AutoKeyRefModule(OptionsModule):
    def __init__(self):
        OptionsModule.__init__(self, options={}, scripts=[join(SCRIPTS_PATH, 'autokey.js')])

    def _get_module(self, request):
        # look for existing values
        try:
            # keyrefId = request.GET['keyref'] if 'keyref' in request.GET else None
            module_id = request.GET['module_id']
            module = data_structure_element_api.get_by_id(module_id)
            keyrefId = module.options['params']['keyref']
            # register the module id in the structure
            if str(module_id) not in request.session['keyrefs'][keyrefId]['module_ids']:
                request.session['keyrefs'][keyrefId]['module_ids'].append(str(module_id))

            # get the list of values for this key
            keyId = request.session['keyrefs'][keyrefId]['refer']
            values = []
            modules_ids = request.session['keys'][keyId]['module_ids']
            for key_module_id in modules_ids:
                key_module = data_structure_element_api.get_by_id(key_module_id)
                if key_module.options['data'] is not None:
                    values.append(key_module.options['data'])

            # add empty value
            self.options.update({'': ''})
            for value in values:
                self.options.update({str(value): str(value)})

            self.selected = ''
            if 'data' in request.GET:
                self.selected = request.GET['data']
            elif 'data' in module.options and module.options['data'] is not None:
                self.selected = str(module.options['data'])
        except Exception:
            self.options = {}
        return OptionsModule.get_module(self, request)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        return self.selected

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        if 'data' in request.POST:
            return request.POST['data']
        return ''
