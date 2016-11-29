from django.conf import settings
from os.path import join, dirname, realpath

if not settings.configured:
    settings.configure()

SITE_ROOT = getattr(settings, 'SITE_ROOT', join(dirname(realpath(__file__))).replace('\\', '/'))

MODULE_ATTRIBUTE = getattr(settings, 'MODULE_ATTRIBUTE', 'module')
