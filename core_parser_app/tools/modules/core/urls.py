from django.conf.urls import patterns, url

urlpatterns = patterns('core_parser_app.tools.modules.core.views',
    url(r'^auto-keyref', 'auto_keyref', name='_auto_keyref'),
    url(r'^get-updated-keys', 'get_updated_keys', name='_get_updated_keys'),
)
