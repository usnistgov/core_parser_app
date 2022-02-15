""" Settings for core_parser_app tests
"""
SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    # 'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    # Local apps
    "tests",
    "core_main_app",
    "core_parser_app",
]

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
    },
]

ROOT_URLCONF = "core_parser_app.urls"
LOGIN_URL = "/login"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
