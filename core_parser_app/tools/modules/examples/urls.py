"""Url routing
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('core_parser_app.tools.modules.examples.views',
    url(r'positive-integer', 'positive_integer',
        name='core_parser_app_example_positive_integer'),
    url(r'autocomplete', 'example_autocomplete',
        name='core_parser_app_example_autocomplete'),
    url(r'chemical-element-mapping', 'chemical_element_mapping',
        name='core_parser_app_example_chemical_element_mapping'),
    url(r'countries-module', 'countries',
        name='Countries'),
    url(r'flag-module', 'flag',
        name='core_parser_app_example_flags'),
    url(r'chemical-element-selection', 'chemical_element_selection',
        name='core_parser_app_example_chemical_element_selection'),
    url(r'^auto-key-randint', 'auto_key_randint',
        name='core_parser_app_example_auto_key_random_integers'),
    url(r'^auto-key-randstr', 'auto_key_randstr',
        name='core_parser_app_example_auto_key_random_strings'),
    url(r'^auto-key-seqint', 'auto_key_int_sequence',
        name='core_parser_app_example_auto_key_sequence_integers'),
)
