"""Url routing
"""
from django.conf.urls import url

import views

urlpatterns = [
    url(r'positive-integer', views.positive_integer,
        name='core_parser_app_example_positive_integer'),
    url(r'autocomplete', views.example_autocomplete,
        name='core_parser_app_example_autocomplete'),
    url(r'chemical-element-mapping', views.chemical_element_mapping,
        name='core_parser_app_example_chemical_element_mapping'),
    url(r'countries-module', views.countries,
        name='Countries'),
    url(r'flag-module', views.flag,
        name='core_parser_app_example_flags'),
    url(r'chemical-element-selection', views.chemical_element_selection,
        name='core_parser_app_example_chemical_element_selection'),
    url(r'^auto-key-randint', views.auto_key_randint,
        name='core_parser_app_example_auto_key_random_integers'),
    url(r'^auto-key-randstr', views.auto_key_randstr,
        name='core_parser_app_example_auto_key_random_strings'),
    url(r'^auto-key-seqint', views.auto_key_int_sequence,
        name='core_parser_app_example_auto_key_sequence_integers'),
]
