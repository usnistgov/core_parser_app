""" Url router for the parser application
"""
from django.conf.urls import url, include
from views.user import ajax as user_ajax

urlpatterns = [
    url(r'^data-structure-element/value', user_ajax.get_data_structure_element_value,
        name='core_parser_app_data_structure_element_value'),

    url(r'^modules/', include('core_parser_app.tools.modules.urls')),
]
