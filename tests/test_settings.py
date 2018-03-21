SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    # Django apps
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    # Local apps
    "tests",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    },
]
