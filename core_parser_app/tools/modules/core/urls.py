from django.conf.urls import patterns, url

urlpatterns = patterns('core_parser_app.tools.modules.core.views',
    url(r'^blob-host', 'blob_host', name='core_parser_app_core_blob_host'),
    url(r'^remote-blob-host', 'remote_blob_host', name='core_parser_app_core_remote_blob_host'),
    url(r'^advanced-blob-host', 'advanced_blob_host', name='core_parser_app_core_advanced_blob_host'),
    url(r'^auto-keyref', 'auto_keyref', name='_auto_keyref'),
    url(r'^get-updated-keys', 'get_updated_keys', name='_get_updated_keys'),
)
