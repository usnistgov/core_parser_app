"""Core modules models
"""
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from core_main_app.components.blob.models import Blob
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.utils import get_blob_download_uri
from core_parser_app.tools.modules.core.forms import BLOBHostForm, URLForm
from core_parser_app.tools.modules.exceptions import ModuleError
from core_parser_app.tools.modules.builtin.models import PopupModule, InputModule
from core_parser_app.settings import MODULES_ROOT
from core_parser_app.tools.modules.builtin.models import OptionsModule
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from os.path import join

RESOURCES_PATH = join(MODULES_ROOT, 'core', 'resources')
TEMPLATES_PATH = join(RESOURCES_PATH, 'html')
SCRIPTS_PATH = join(RESOURCES_PATH, 'js')
STYLES_PATH = join(RESOURCES_PATH, 'css')


class BlobHostModule(PopupModule):
    """BLOB host module
    """
    def __init__(self):
        """Initialize module
        """
        self.handle = None

        with open(join(TEMPLATES_PATH, 'blob_host.html'), 'r') as blob_host_file:
            blob_host = blob_host_file.read()
            template = Template(blob_host)
            context = Context({'form': BLOBHostForm()})
            popup_content = template.render(context)

        PopupModule.__init__(self, popup_content=popup_content, button_label='Upload File',
                             scripts=[join(SCRIPTS_PATH, 'blob_host.js')])

    def _get_module(self, request):
        """ Get module
        Args:
            request:

        Returns:

        """
        return PopupModule.get_module(self, request)

    def _get_display(self, request):
        """ Return module display - GET method

        Args:
            request:

        Returns:

        """
        if 'data' in request.GET:
            if len(request.GET['data']) > 0:
                return '<b>Handle: </b> <a href="' + request.GET['data'] + '">' + request.GET['data'] + '</a>'
        return 'No files selected'

    def _get_result(self, request):
        """ Return module result - GET method

        Args:
            request:

        Returns:

        """
        if 'data' in request.GET:
            if len(request.GET['data']) > 0:
                return request.GET['data']
        return ''

    def _post_display(self, request):
        """ Return module display - POST method

        Args:
            request:

        Returns:

        """
        form = BLOBHostForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ModuleError('Data not properly sent to server. Please provide "file" in POST data.')

        # get file from request
        uploaded_file = request.FILES['file']
        # get filename from file
        filename = uploaded_file.name
        # get user id from request
        user_id = str(request.user.id)

        # create blob
        blob = Blob(filename=filename, user_id=user_id)
        # set blob file
        blob.blob = uploaded_file
        # save blob
        blob_api.save(blob)

        # get download uri
        self.handle = get_blob_download_uri(blob, request)

        with open(join(TEMPLATES_PATH, 'blob_host_display.html'), 'r') as display_file:
            display = display_file.read()
            template = Template(display)
            context = Context({'filename': filename, 'handle': self.handle})

        return template.render(context)

    def _post_result(self, request):
        """Return module result - POST method

        Args:
            request:

        Returns:

        """
        return self.handle if self.handle is not None else ''


class RemoteBlobHostModule(InputModule):
    def __init__(self):
        """ Initialize the module
        """
        self.handle = None

        InputModule.__init__(self, label='Enter the URL of a file:')

    def _get_module(self, request):
        """ Get module

        Args:
            request:

        Returns:

        """
        return InputModule.get_module(self, request)

    def _get_display(self, request):
        """ Return module display - GET method

        Args:
            request:

        Returns:

        """
        if 'data' in request.GET:
            if len(request.GET['data']) > 0:
                return '<b>Handle: </b> <a href="' + request.GET['data'] + '">' + request.GET['data'] + '</a>'
        return 'No files selected'

    def _get_result(self, request):
        """ Return module result - GET method

        Args:
            request:

        Returns:

        """
        if 'data' in request.GET:
            if len(request.GET['data']) > 0:
                return request.GET['data']
        return ''

    def _post_display(self, request):
        """ Return module display - POST method

        Args:
            request:

        Returns:

        """
        url = ''
        if 'data' in request.POST:
            url = request.POST['data']

        url_validator = URLValidator()
        self.handle = ''
        try:
            url_validator(url)
            self.handle = url
            with open(join(TEMPLATES_PATH, 'remote_blob_host_display.html'), 'r') as display_file:
                display = display_file.read()
                template = Template(display)
                context = Context({'handle': url})
            return template.render(context)
        except ValidationError, e:
            return '<b style="color:red;">' + '<br/>'.join(e.messages) + '</b>'

    def _post_result(self, request):
        """ Return module result - POST method

        Args:
            request:

        Returns:

        """
        return self.handle if self.handle is not None else ''


class AdvancedBlobHostModule(PopupModule):
    def __init__(self):
        """Initialize module

        """
        self.handle = None

        with open(join(TEMPLATES_PATH, 'advanced_blob_host.html'), 'r') as blob_host_file:
            blob_host = blob_host_file.read()
            template = Template(blob_host)
            context = Context({'url_form': URLForm(), 'file_form': BLOBHostForm()})
            popup_content = template.render(context)

        PopupModule.__init__(self, popup_content=popup_content, button_label='Upload File',
                             scripts=[join(SCRIPTS_PATH, 'advanced_blob_host.js')])

    def _get_module(self, request):
        """ Get module

        Args:
            request:

        Returns:

        """
        return PopupModule.get_module(self, request)

    def _get_display(self, request):
        """ Return module display - GET method

        Args:
            request:

        Returns:

        """
        if 'data' in request.GET:
            if len(request.GET['data']) > 0:
                return '<b>Handle: </b> <a href="' + request.GET['data'] + '">' + request.GET['data'] + '</a>'
        return 'No files selected'

    def _get_result(self, request):
        """ Return module result - GET method

        Args:
            request:

        Returns:

        """
        if 'data' in request.GET:
            if len(request.GET['data']) > 0:
                return request.GET['data']
        return ''

    def _post_display(self, request):
        """ Return module display - POST method

        Args:
            request:

        Returns:

        """
        self.handle = ''
        selected_option = request.POST['blob_form']
        if selected_option == "url":
            url_form = URLForm(request.POST)
            if url_form.is_valid():
                self.handle = url_form.data['url']
                with open(join(TEMPLATES_PATH, 'remote_blob_host_display.html'), 'r') as display_file:
                    display = display_file.read()
                    template = Template(display)
                    context = Context({'handle': self.handle})
                return template.render(context)
            else:
                return '<b style="color:red;">Enter a valid URL.</b>'
        elif selected_option == "file":
            # get file from request
            uploaded_file = request.FILES['file']
            # get filename from file
            filename = uploaded_file.name
            # get user id from request
            user_id = str(request.user.id)

            # create blob
            blob = Blob(filename=filename, user_id=user_id)
            # set blob file
            blob.blob = uploaded_file
            # save blob
            blob_api.save(blob)

            # get download uri
            self.handle = get_blob_download_uri(blob, request)

            with open(join(TEMPLATES_PATH, 'blob_host_display.html'), 'r') as display_file:
                display = display_file.read()
                template = Template(display)
                context = Context({'filename': filename, 'handle': self.handle})

            return template.render(context)

    def _post_result(self, request):
        """ Return module result - POST method

        Args:
            request:

        Returns:

        """
        return self.handle if self.handle is not None else ''


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
