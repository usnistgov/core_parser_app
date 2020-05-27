"""Url routing
"""

from django.urls import re_path

from core_parser_app.tools.modules.views import views as modules_views

urlpatterns = [
    re_path(r"^$", modules_views.index, name="core_parser_app_modules"),
    re_path(
        r"^resources",
        modules_views.load_resources_view,
        name="core_parser_app_modules_resources",
    ),
]
