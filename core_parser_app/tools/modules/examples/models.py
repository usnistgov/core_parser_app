"""Example modules classes
"""
from core_parser_app.tools.modules.builtin.models import InputModule, OptionsModule, AutoCompleteModule, \
    CheckboxesModule
from core_parser_app.tools.modules.module import AbstractModule
from core_parser_app.tools.modules.xpathaccessor import XPathAccessor
from core_parser_app.settings import MODULES_ROOT
import os


RESOURCES_PATH = os.path.join(MODULES_ROOT, 'examples', 'resources')
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'html')
SCRIPTS_PATH = os.path.join(RESOURCES_PATH, 'js')
STYLES_PATH = os.path.join(RESOURCES_PATH, 'css')


class PositiveIntegerInputModule(InputModule):
    """Positive integer module - input module
    """
    def __init__(self):
        """

        """
        InputModule.__init__(self, label='Enter positive integer', default_value=1)

    def _get_module(self, request):
        """

        :param request:
        :return:
        """
        if 'data' in request.GET:
            self.default_value = request.GET['data']

        return InputModule.get_module(self, request)

    @staticmethod
    def is_data_valid(self, data):
        """

        :param data:
        :return:
        """
        try:
            value = int(data)
            if value >= 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def _get_display(self, request):
        """

        :param request:
        :return:
        """
        if 'data' in request.GET:
            data = str(request.GET['data'])
            return data + " is a positive integer" if self.is_data_valid(data) else \
                "<div style='color:red;'>This is not a positive integer</div>"
        return str(self.default_value) + ' is a positive integer'

    def _get_result(self, request):
        """

        :param request:
        :return:
        """
        if 'data' in request.GET:
            return str(request.GET['data'])
        return str(self.default_value)

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        data = str(request.POST['data'])
        return data + " is a positive integer" if self.is_data_valid(data) \
            else "<div style='color:red;'>This is not a positive integer</div>"

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        return str(request.POST['data'])


class ChemicalElementMappingModule(OptionsModule):
    """Chemical Element mapping module - use of options module
    """
    def __init__(self):
        """

        """
        self.options = {
            'Ac': 'Actinium',
            'Al': 'Aluminum',
            'Ag': 'Silver',
            'Am': 'Americium',
            'Ar': 'Argon',
            'As': 'Arsenic',
            'At': 'Astatine',
            'Au': 'Gold'
        }
                
        OptionsModule.__init__(self, options=self.options, label='Select an element')

    def _get_module(self, request):
        """

        :param request:
        :return:
        """
        return OptionsModule.get_module(self, request)

    def _get_display(self, request):
        """

        :param request:
        :return:
        """
        return self.options.values()[0] + ' is selected'

    def _get_result(self, request):
        """

        :param request:
        :return:
        """
        return self.options.keys()[0]

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        data = str(request.POST['data'])
        return self.options[data] + ' is selected'

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        return str(request.POST['data'])


# FIXME: Module not working
class ExampleAutoCompleteModule(AutoCompleteModule):
    """Example of autocomplete module - use of autocomplete
    """
    def __init__(self):
        """

        """
        self.data = [
            'Plastic',
            'Concrete',
            'Cement',
            'Material1',
            'Material2',
            'Material3',
            'Others'
        ]

        AutoCompleteModule.__init__(self, label='Material Name', scripts=[os.path.join(SCRIPTS_PATH,
                                                                                       'example_autocomplete.js')])

    def _get_module(self, request):
        """

        :param request:
        :return:
        """
        return AutoCompleteModule.get_module(self, request)

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
        return ''

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        if 'list' in request.POST:
            response_list = []

            for term in self.data:
                if request.POST['list'].lower() in term.lower():
                    response_list.append(term)

            return response_list

        if 'data' in request.POST:
            return request.POST['data']

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        if 'data' in request.POST:
            return request.POST['data']

        return ''


class CountriesModule(OptionsModule, XPathAccessor):
    """Countries module - use of XpathAccessor
    """
    country_codes = {
                     'None': '',
                     'FRANCE': 'FR',
                     'UNITED STATES OF AMERICA': 'USA',
                     }
    
    capitals = {
                'None': '',
                'FRANCE': 'PARIS',
                'UNITED STATES OF AMERICA': 'WASHINGTON DC',
                }
    
    anthems = {
               'None': '',
               'FRANCE': 'La Marseillaise',
               'UNITED STATES OF AMERICA': 'The Star-Sprangled Banner',
               }
    
    flags = {
             'None': 'None',
             'FRANCE': 'Tricolour',
             'UNITED STATES OF AMERICA': 'The Stars and Stripes',
             }
    
    languages = {
             'None': '',
             'FRANCE': 'FRENCH',
             'UNITED STATES OF AMERICA': 'ENGLISH',
             }
    
    def __init__(self):
        self.options = {
            'None': '--------',
            'FRANCE': 'France',
            'UNITED STATES OF AMERICA': 'USA',
        }
                
        OptionsModule.__init__(self, options=self.options, label='Select a Country',
                               scripts=[os.path.join(SCRIPTS_PATH, 'countries.js')])

    def _get_module(self, request):
        return OptionsModule.get_module(self, request)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):     
        if 'data' in request.GET:
            return str(request.GET['data'])
        return ''

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        # get the selected value
        value = str(request.POST['data'])
        
        # create the XPathAccessor
        XPathAccessor.__init__(self, request)
        
        return value
        
    def set_XpathAccessor(self, request):
        # get the selected value
        if 'data' not in request.POST:
            return

        value = str(request.POST['data'])

        if value not in self.country_codes.keys():  # FIXME loose test, fix datastrcture
            return
        
        # get values to return for siblings
        country_code = self.country_codes[value]
        capital = self.capitals[value]
        anthem = self.anthems[value]
        language = self.languages[value]
        flag = self.flags[value]
         
        # get xpath of current node (for dynamic xpath building)
        module_xpath = self.get_xpath()
        parent_xpath = "/".join(module_xpath.split("/")[:-1])
        parent_xpath_idx = parent_xpath[parent_xpath.rfind("[")+1:-1]
        idx = "[" + str(parent_xpath_idx) + "]"
         
        # set nodes with values
        form_id = request.session['form_id']

        self.set_xpath_value(form_id, '/Countries[1]/country' + idx + '/country_code', country_code)
        self.set_xpath_value(form_id, '/Countries[1]/country' + idx + '/details[1]/capital', capital)
        self.set_xpath_value(form_id, '/Countries[1]/country' + idx + '/details[1]/anthem', anthem)
        self.set_xpath_value(form_id, '/Countries[1]/country' + idx + '/details[1]/language', language)
        self.set_xpath_value(form_id, '/Countries[1]/country' + idx + '/details[1]/flag', {'data': flag})


class FlagModule(AbstractModule):
    """Flag module - use of XpathAccessor
    """
    
    images = {
        'The Stars and Stripes': "<img src='https://upload.wikimedia.org/wikipedia/en/a/a4/"
                                 "Flag_of_the_United_States.svg' height='42' width='42'/>",
        'Tricolour': "<img src='https://upload.wikimedia.org/wikipedia/commons/c/c3/"
                     "Flag_of_France.svg' height='42' width='42'/>"
    }
    
    def __init__(self):
        AbstractModule.__init__(self)

    def _get_module(self, request):
        return ''

    def _get_display(self, request):
        if 'data' in request.GET:
            image_id = str(request.GET['data'])

            if image_id in self.images.keys():
                return self.images[image_id]

        return ''

    def _get_result(self, request):
        if 'data' in request.GET:
            return str(request.GET['data'])
        return ''

    def _post_display(self, request):
        if 'data' in request.POST:
            image_id = str(request.POST['data'])

            if image_id in self.images.keys():
                return self.images[image_id]

        return ''

    def _post_result(self, request):
        return str(request.POST['data'])


class ChemicalElementCheckboxesModule(CheckboxesModule):
    """Chemical element checkboxes module - use of checkbox module
    """
    
    def __init__(self):
        self.options = {
            'Ac': 'Actinium',
            'Al': 'Aluminum',
            'Ag': 'Silver',
            'Am': 'Americium',
            'Ar': 'Argon',
            'As': 'Arsenic',
            'At': 'Astatine',
            'Au': 'Gold'
        }
                
        CheckboxesModule.__init__(self, options=self.options, label='Select elements', name='chemical')

    def _get_module(self, request):
        """

        :param request:
        :return:
        """
        return CheckboxesModule.get_module(self, request)

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
        return ''

    def _post_display(self, request):
        """

        :param request:
        :return:
        """
        return ''

    def _post_result(self, request):
        """

        :param request:
        :return:
        """
        if 'data[]' in request.POST:
            return str(request.POST['data[]'])
