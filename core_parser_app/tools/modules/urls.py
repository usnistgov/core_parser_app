"""Url routing
"""
from django.conf.urls import patterns, include, url

urlpatterns = [
    url(r'^resources$', 'core_parser_app.tools.modules.views.load_resources_view', name='load_resources'),
    url(r'^examples/', include('core_parser_app.tools.modules.examples.urls')),
]

excluded = ['load_resources', '_get_updated_keys']
