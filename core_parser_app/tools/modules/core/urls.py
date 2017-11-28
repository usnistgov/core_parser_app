from django.conf.urls import url

from core_parser_app.tools.modules.core import views

urlpatterns = [
    url(r'^blob-host', views.blob_host,
        name='core_parser_app_core_blob_host'),
    url(r'^remote-blob-host', views.remote_blob_host,
        name='core_parser_app_core_remote_blob_host'),
    url(r'^advanced-blob-host', views.advanced_blob_host,
        name='core_parser_app_core_advanced_blob_host'),
    url(r'^auto-keyref', views.auto_keyref,
        name='_auto_keyref'),
    url(r'^get-updated-keys', views.get_updated_keys,
        name='_get_updated_keys'),
]
