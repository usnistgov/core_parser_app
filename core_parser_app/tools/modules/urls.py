"""Url routing
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'^resources$', 'core_parser_app.tools.modules.views.load_resources_view', name='load_resources'),
    url(r'^examples/', include('core_parser_app.tools.modules.examples.urls')),
    url(r'^core/', include('core_parser_app.tools.modules.core.urls')),
]

excluded = ['load_resources', '_get_updated_keys']
